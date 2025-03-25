"""
Learning Portal - RAG Agent Implementation

This module implements the Retrieval Augmented Generation (RAG) agent
using LangGraph, LangChain, and the Qdrant vector database.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from typing import Dict, TypedDict, List, Tuple, Annotated, Union, Optional
from langgraph.graph import Graph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings, logger
from app.db.qdrant import init_vector_store, get_collection_name
from app.models.schema import HistoryItem

# Define state structure for the LangGraph agent
# This maintains conversation context and retrieved information
class AgentState(TypedDict):
    messages: List[str]     # Conversation messages
    context: List[str]      # Retrieved context from vector store
    references: List[Dict]  # Source references for citations

# Retrieval node for the RAG pattern
# Searches for relevant documents based on the user's query
def retrieve_node(state: AgentState) -> AgentState:
    """
    Retrieve relevant context from the vector store based on the query.
    """
    last_message = state["messages"][-1]
    
    # Get module from state (with default for backward compatibility)
    module = state.get("module", "module1")
    
    # Generate collection name
    collection_name = get_collection_name(module)
    
    try:
        # Initialize vector store
        _, client = init_vector_store(collection_name)
        
        # Log only the essential information about the query
        logger.info(f"Embedding query for collection '{collection_name}': {last_message[:50]}...")
        
        # Generate query embedding for semantic search
        embeddings = OpenAIEmbeddings()
        query_vector = embeddings.embed_query(last_message)
        
        # Perform semantic search in Qdrant
        # Returns documents with similarity score > 0.7
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=10,  # Retrieve top 10 most relevant documents
            score_threshold=0.7  # Minimum similarity threshold
        )
        
        if not search_result:
            logger.info("No relevant documents found for query")
            state["context"] = ["No relevant information found in the documents."]
            state["references"] = []
        else:
            # Only log the number of documents found, not all details
            logger.info(f"Found {len(search_result)} relevant documents for query")
            
            # Extract content and metadata from search results
            contexts = []
            references = []
            for i, hit in enumerate(search_result):
                if hit.payload and "page_content" in hit.payload:
                    contexts.append(hit.payload["page_content"])
                    text_excerpt = hit.payload["page_content"][:200] + "..."
                    references.append({
                        "text": text_excerpt,
                        "document": hit.payload.get("metadata", {}).get("source", "").split("/")[-1],
                        "page": hit.payload.get("metadata", {}).get("page", 0)
                    })
            
            # Update state with retrieved context and references
            state["context"] = contexts if contexts else ["No readable content found in the documents."]
            state["references"] = references
    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}")
        state["context"] = ["Error retrieving information from documents."]
        state["references"] = []
    return state

# Response generation function
def generate_response(state: AgentState) -> AgentState:
    """
    Generate a response based on the retrieved context and query.
    """
    # Create prompt with system instruction and context
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant specialized in analyzing information and answering questions. 
        Format your responses in markdown to make them visually appealing and easy to read.
        Use the following context to answer the question.
        
        Context: {context}"""),
        ("human", "{question}")
    ])
    
    # Create LLM instance
    llm = ChatOpenAI(model="gpt-4")
    
    # Create chain combining prompt and language model
    chain = prompt | llm
    
    # Prepare inputs from agent state
    context = "\n\n".join(state["context"]) if state["context"] else "No context available."
    question = state["messages"][-1]
    
    # Log the OpenAI API call for monitoring
    logger.info(f"OpenAI API Call - Model: gpt-4 - Prompt: System prompt with context and question: '{question[:50]}...'")
    
    # Generate response
    response = chain.invoke({
        "context": context,
        "question": question
    })
    
    # Add response to messages
    state["messages"].append(response.content)
    return state

# Create LangGraph agent for orchestrating the RAG workflow
def create_agent():
    """
    Create a LangGraph agent for RAG workflow.
    """
    # Define workflow
    workflow = Graph()
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_response)
    
    # Add edges
    workflow.add_edge("retrieve", "generate")
    
    # Set entry point and end node
    workflow.set_entry_point("retrieve")
    workflow.set_finish_point("generate")
    
    # Compile with config to ensure state is returned
    return workflow.compile()

def get_qdrant_response(question: str, module: str = "module1", unit: Optional[str] = None, history: List[HistoryItem] = None) -> Dict:
    """
    Get a response from the RAG agent based on a question and conversation history.
    """
    # Initialize agent
    chain = create_agent()
    
    # Initialize state with message history
    messages = []
    
    # Add conversation history if available
    if history:
        for item in history:
            messages.append(item.content)
    
    # Add current question to messages
    messages.append(question)
    
    # Initialize state
    state = {
        "messages": messages,
        "context": [],
        "references": [],
        "module": module,
        "unit": unit
    }
    
    # Run chain with state
    try:
        result = chain.invoke(state)
        
        # Return response with references
        return {
            "answer": result["messages"][-1],
            "references": result["references"]
        }
    except Exception as e:
        logger.error(f"Error in RAG agent: {str(e)}")
        return {
            "answer": "I'm sorry, I encountered an error while processing your question.",
            "references": []
        }

# Implement the streaming response function
async def get_qdrant_response_stream(question: str, module: str = "module1", unit: Optional[str] = None, history: List[HistoryItem] = None):
    """
    Get a streaming response from the RAG agent.
    """
    # This is a placeholder for the streaming implementation
    # In a real implementation, this would use async generators with SSE
    
    # For now, we'll simulate streaming by getting the full response
    # and yielding it in chunks
    response = get_qdrant_response(question, module, unit, history)
    
    # Yield the response as JSON in Server-Sent Events format
    yield f"data: {{'content': '{response['answer']}'}}\n\n"
    
    # Done event
    yield "data: {'done': true}\n\n"

# Function for analyzing user answers
async def get_answer_analysis(question: str, user_answer: str, guide: str, module: str = "module1", unit: Optional[str] = None) -> Dict:
    """
    Analyze a user's answer against a guide and relevant context.
    """
    # Initialize vector store
    vector_store, _ = init_vector_store(get_collection_name(module))
    
    # Search for relevant context based on the question
    context_docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in context_docs])
    
    # Create prompt with system instruction and context
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an educational assessment AI. Analyze the user's answer to the given question.
        Compare it against both the evaluation guide and the relevant factual context.
        
        Format your analysis as markdown and include:
        1. A summary of what the answer covered well
        2. Key points that were missed or could be improved
        3. Factual accuracy assessment
        4. A numeric score from 0-100
        
        Question: {question}
        User Answer: {user_answer}
        Evaluation Guide: {guide}
        Relevant Context: {context}"""),
        ("human", "Please analyze this answer comprehensively.")
    ])
    
    # Create LLM instance and chain
    llm = ChatOpenAI(model="gpt-4")
    chain = prompt | llm
    
    # Generate analysis
    try:
        response = chain.invoke({
            "question": question,
            "user_answer": user_answer,
            "guide": guide,
            "context": context
        })
        
        # Extract score from the response if present
        content = response.content
        score = 0
        
        # Simple regex to find the score
        import re
        score_match = re.search(r'score[:\s]*(\d+)', content, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))
            if score < 0:
                score = 0
            elif score > 100:
                score = 100
        
        return {
            "analysis": content,
            "score": score
        }
    except Exception as e:
        logger.error(f"Error in answer analysis: {str(e)}")
        return {
            "analysis": "I'm sorry, I encountered an error while analyzing your answer.",
            "score": 0
        }

# Streaming version of the analysis function
async def get_streaming_analysis(question: str, user_answer: str, guide: str, module: str = "module1", unit: Optional[str] = None):
    """
    Get a streaming analysis of a user's answer.
    """
    # This is a placeholder for the streaming implementation
    # In a real implementation, this would use async generators with SSE
    
    # For now, we'll simulate streaming by getting the full analysis
    # and yielding it in chunks
    response = await get_answer_analysis(question, user_answer, guide, module, unit)
    
    # Yield the analysis as JSON in Server-Sent Events format
    yield f"data: {{'content': '{response['analysis']}'}}\n\n"
    
    # Yield the score
    yield f"data: {{'score': {response['score']}}}\n\n"
    
    # Done event
    yield "data: {'done': true}\n\n" 