"""
Learning Portal - Data Models

This module defines the Pydantic data models used throughout the application
for request validation and response structuring.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Union

# Represents a single message in the conversation history
# Used to maintain context in multi-turn conversations
class HistoryItem(BaseModel):
    content: str    # The text content of the message
    isBot: bool     # Flag indicating if the message is from the bot (True) or user (False)

# Represents a question sent to the bot
# Contains the question text and optional conversation history
class Question(BaseModel):
    text: str       # The question text being asked
    module: str = Field(default="module1", description="Module identifier (e.g., 'module1')")  # Learning module identifier
    history: Optional[List[HistoryItem]] = []  # Previous conversation history for context

# Represents a request to analyze a user's answer to a question
# Used in assessment/feedback functionality
class AnswerAnalysis(BaseModel):
    question: str = Field(..., description="The question asked")  # Original question text
    user_answer: str = Field(..., description="The answer provided by the user")  # User's submitted answer
    module: str = Field(default="module1", description="Module identifier (e.g., 'module1')")  # Learning module identifier
    guide: str = Field(..., description="Guidelines for what the answer should contain")  # Assessment criteria

# Response model for the answer analysis
# Contains the detailed analysis of the user's answer
class AnalysisResponse(BaseModel):
    analysis: Dict = Field(..., description="Analysis of the user's answer")  # Structured analysis data 

# Represents information about a chatbot/module
class ChatbotInfo(BaseModel):
    id: str = Field(..., description="Unique identifier for the chatbot (module name)")
    name: str = Field(..., description="Display name for the chatbot")
    description: str = Field(..., description="Description of the chatbot's capabilities")
    icon: str = Field("🤖", description="Emoji or icon identifier for the chatbot") 