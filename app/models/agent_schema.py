"""
Learning Portal - Agent Pydantic Schemas

This module defines Pydantic models for agent-related API operations.

Author: Abhijit Raijada
Designation: Principle Engineer
Organization: GRS
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

# ===== PUBLIC SCHEMAS (Regular Users) =====

class PublicChatbotInfo(BaseModel):
    """Limited chatbot info for regular users - no sensitive data exposed"""
    id: str = Field(..., description="Agent identifier for chat")
    name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Brief description")
    icon: str = Field(default="robot", description="Display icon")

class ChatRequest(BaseModel):
    """Chat request from users"""
    agent_id: str = Field(..., description="Selected agent ID")
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    history: Optional[List[Dict]] = Field(default=[], description="Chat history")

# ===== ADMIN SCHEMAS (Admin/Superadmin Users) =====

class AgentCreate(BaseModel):
    """Schema for creating new agents"""
    id: str = Field(..., pattern="^[a-zA-Z0-9_-]+$", min_length=1, max_length=50, 
                   description="Unique identifier (alphanumeric, underscore, dash only)")
    name: str = Field(..., min_length=1, max_length=100, description="Display name")
    description: Optional[str] = Field(None, max_length=1000, description="Agent description")
    system_prompt: str = Field(..., min_length=10, max_length=5000, 
                              description="System prompt for agent behavior")
    icon: str = Field(default="robot", max_length=10, description="Emoji icon")
    qdrant_collection: Optional[str] = Field(None, max_length=100, 
                                           description="Specific Qdrant collection to use")
    is_active: bool = Field(default=True, description="Whether agent is active")

class AgentUpdate(BaseModel):
    """Schema for updating existing agents"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    system_prompt: Optional[str] = Field(None, min_length=10, max_length=5000)
    icon: Optional[str] = Field(None, max_length=10)
    qdrant_collection: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class AdminAgentResponse(BaseModel):
    """Complete agent information for admins"""
    id: str
    name: str
    description: Optional[str]
    system_prompt: str
    icon: str
    qdrant_collection: Optional[str]
    is_active: bool
    created_by: int
    creator_name: Optional[str] = None  # Will be populated via join
    created_at: datetime
    updated_at: Optional[datetime]
    usage_stats: Optional[Dict] = None  # Chat count, last used, etc.

    class Config:
        from_attributes = True

class AgentTestRequest(BaseModel):
    """Schema for testing agent configuration"""
    test_message: str = Field(..., min_length=1, max_length=500, 
                             description="Test message to send to agent")
    test_history: Optional[List[Dict]] = Field(default=[], 
                                              description="Optional test conversation history")

class AgentTestResponse(BaseModel):
    """Response from agent testing"""
    agent_id: str
    test_message: str
    response: str
    response_time_ms: int
    success: bool
    error: Optional[str] = None

# ===== UTILITY SCHEMAS =====

class AgentUsageStats(BaseModel):
    """Agent usage statistics"""
    total_conversations: int = 0
    total_messages: int = 0
    last_used: Optional[datetime] = None
    avg_response_time_ms: Optional[float] = None
    user_satisfaction_score: Optional[float] = None

class BulkAgentOperation(BaseModel):
    """Schema for bulk operations on agents"""
    agent_ids: List[str] = Field(..., min_items=1, max_items=50)
    operation: str = Field(..., pattern="^(activate|deactivate|delete)$")
    
class AgentListResponse(BaseModel):
    """Response for paginated agent lists"""
    agents: List[AdminAgentResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool 