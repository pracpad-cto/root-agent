"""
Learning Portal - RAG Agent Implementation

This module implements the Retrieval Augmented Generation (RAG) agent
using LangGraph, LangChain, and the Qdrant vector database with dynamic agent configurations.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from typing import Dict, TypedDict, List, Tuple, Annotated, Union, Optional, Any
from langgraph.graph import Graph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings, logger
from app.db.qdrant import init_vector_store, get_collection_name
from app.models.schema import HistoryItem

# Define state structure for the LangGraph agent
# This maintains conversation context, retrieved information, and agent configuration
class AgentState(TypedDict):
    messages: List[str]     # Conversation messages
    context: List[str]      # Retrieved context from vector store
    references: List[Dict]  # Source references for citations
    agent_config: Dict[str, Any]  # Dynamic agent configuration

# Retrieval node for the RAG pattern
# Searches for relevant documents based on the user's query and agent configuration
def retrieve_node(state: AgentState) -> AgentState:
    """
    Retrieve relevant context from the vector store based on the query and agent config.
    """
    last_message = state["messages"][-1]
    agent_config = state.get("agent_config", {})
    
    # Get collection from agent config, with fallback to module or default
    collection_name = None
    if agent_config.get("qdrant_collection"):
        collection_name = agent_config["qdrant_collection"]
    else:
        # Fallback to old module-based approach for backward compatibility
        module = state.get("module", "module1")
        collection_name = get_collection_name(module)
    
    try:
        # Initialize vector store
        _, client = init_vector_store(collection_name)
        
        # Log retrieval information
        agent_name = agent_config.get("agent_name", "Unknown Agent")
        logger.info(f"Retrieving for agent '{agent_name}' from collection '{collection_name}': {last_message[:50]}...")
        
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
            # Log the number of documents found
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

# Response generation function with dynamic system prompts
def generate_response(state: AgentState) -> AgentState:
    """
    Generate a response based on the retrieved context, query, and agent configuration.
    """
    agent_config = state.get("agent_config", {})
    
    # Get dynamic system prompt or use default
    system_prompt = agent_config.get("system_prompt", 
        """You are a helpful AI assistant specialized in analyzing information and answering questions. 
        Format your responses in markdown to make them visually appealing and easy to read.
        Use the following context to answer the question.
        
        Context: {context}""")
    
    # Create prompt with dynamic system instruction and context
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\n\nContext: {context}"),
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
    agent_name = agent_config.get("agent_name", "Unknown Agent")
    logger.info(f"OpenAI API Call - Agent: {agent_name} - Model: gpt-4 - Question: '{question[:50]}...'")
    
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

# NEW: Dynamic agent response function
def get_agent_response(question: str, agent_config: Dict[str, Any], history: List = None) -> Dict:
    """
    Get a response from the RAG agent using dynamic agent configuration.
    
    Args:
        question: User's question
        agent_config: Dynamic agent configuration with system_prompt, collection, etc.
        history: Conversation history
        
    Returns:
        Response dictionary with answer and references
    """
    # Initialize agent
    chain = create_agent()
    
    # Initialize state with message history
    messages = []
    
    # Add conversation history if available
    if history:
        for item in history:
            if isinstance(item, dict):
                messages.append(item.get('content', str(item)))
            else:
                messages.append(str(item))
    
    # Add current question to messages
    messages.append(question)
    
    # Initialize state with agent configuration
    state = {
        "messages": messages,
        "context": [],
        "references": [],
        "agent_config": agent_config
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
        agent_name = agent_config.get("agent_name", "Unknown Agent")
        logger.error(f"Error in RAG agent '{agent_name}': {str(e)}")
        return {
            "answer": "I'm sorry, I encountered an error while processing your question.",
            "references": []
        }

# NEW: Streaming response with dynamic agent configuration
async def get_agent_response_stream(question: str, agent_config: Dict[str, Any], history: List = None):
    """
    Get a streaming response from the RAG agent using dynamic agent configuration.
    
    Args:
        question: User's question
        agent_config: Dynamic agent configuration
        history: Conversation history
        
    Yields:
        Response chunks for streaming
    """
    # Get the full response first
    response = get_agent_response(question, agent_config, history)
    answer = response['answer']
    
    # Properly escape content to avoid issues with quotes and special characters
    import json
    
    # Split response into smaller chunks (sentences or parts)
    import re
    # Split by sentence endings or markdown headers
    chunks = re.split(r'(?<=[.!?])\s+|\n(?=#+\s+)', answer)
    
    # Send each chunk separately for a smoother streaming experience
    for chunk in chunks:
        if chunk.strip():  # Only send non-empty chunks
            content_json = json.dumps({"content": chunk + " "})  # Add space after each chunk
            yield f"data: {content_json}\n\n"
            # Small delay to simulate streaming (optional)
            import asyncio
            await asyncio.sleep(0.1)
    
    # Done event
    done_json = json.dumps({"done": True})
    yield f"data: {done_json}\n\n"

# BACKWARD COMPATIBILITY: Keep existing functions for legacy support
def get_qdrant_response(question: str, module: str = "module1", history: List[HistoryItem] = None) -> Dict:
    """
    Get a response from the RAG agent based on a question and conversation history.
    [LEGACY] This function is maintained for backward compatibility.
    """
    # Create a default agent config for backward compatibility
    agent_config = {
        "agent_name": "Legacy Agent",
        "system_prompt": """You are a helpful AI assistant specialized in analyzing information and answering questions. 
        Format your responses in markdown to make them visually appealing and easy to read.
        Use the following context to answer the question.""",
        "qdrant_collection": None,  # Will use module-based collection
        "module": module
    }
    
    return get_agent_response(question, agent_config, history)

async def get_qdrant_response_stream(question: str, module: str = "module1", history: List[HistoryItem] = None):
    """
    Get a streaming response from the RAG agent.
    [LEGACY] This function is maintained for backward compatibility.
    """
    # Create a default agent config for backward compatibility
    agent_config = {
        "agent_name": "Legacy Agent",
        "system_prompt": """You are a helpful AI assistant specialized in analyzing information and answering questions. 
        Format your responses in markdown to make them visually appealing and easy to read.
        Use the following context to answer the question.""",
        "qdrant_collection": None,  # Will use module-based collection
        "module": module
    }
    
    async for chunk in get_agent_response_stream(question, agent_config, history):
        yield chunk

# Function for analyzing user answers (unchanged for now)
async def get_answer_analysis(question: str, user_answer: str, guide: str, module: str = "module1") -> Dict:
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
async def get_streaming_analysis(question: str, user_answer: str, guide: str, module: str = "module1"):
    """
    Get a streaming analysis of a user's answer.
    """
    # This is a placeholder for the streaming implementation
    # In a real implementation, this would use async generators with SSE
    
    # For now, we'll simulate streaming by getting the full analysis
    # and yielding it in chunks
    response = await get_answer_analysis(question, user_answer, guide, module)
    
    # Properly escape content to avoid issues with quotes and special characters
    import json
    
    # Yield the analysis as JSON in Server-Sent Events format
    content_json = json.dumps({"content": response['analysis']})
    yield f"data: {content_json}\n\n"
    
    # Yield the score
    score_json = json.dumps({"score": response['score']})
    yield f"data: {score_json}\n\n"
    
    # Done event
    done_json = json.dumps({"done": True})
    yield f"data: {done_json}\n\n" 