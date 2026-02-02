"""MongoDB memory management for agents."""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)


class MongoMemory:
    """MongoDB-based memory for agent state and history."""
    
    def __init__(self, mongo_uri: str, database: str = "agent_memory"):
        """Initialize MongoDB connection.
        
        Args:
            mongo_uri: MongoDB connection URI
            database: Database name
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database]
        self.interactions = self.db["interactions"]
        self.sessions = self.db["sessions"]
        
        # Create indexes (ignore if already exists)
        try:
            self.interactions.create_index([("session_id", 1), ("timestamp", -1)])
        except Exception:
            pass
        
        try:
            self.sessions.create_index("session_id")
        except Exception:
            pass
        
        logger.info("✅ MongoDB memory initialized")
    
    def save_interaction(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Save an interaction to memory.
        
        Args:
            session_id: Session identifier
            role: Role (user, assistant, orchestrator, agent)
            content: Content of the interaction
            metadata: Additional metadata
            
        Returns:
            Inserted document ID
        """
        doc = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        
        result = self.interactions.insert_one(doc)
        return str(result.inserted_id)
    
    def get_session_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get interaction history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of interactions to return
            
        Returns:
            List of interaction documents
        """
        query = {"session_id": session_id}
        cursor = self.interactions.find(query).sort("timestamp", 1)
        
        if limit:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def create_session(
        self,
        session_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new session.
        
        Args:
            session_id: Session identifier
            metadata: Session metadata
            
        Returns:
            Session ID
        """
        doc = {
            "session_id": session_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "metadata": metadata or {},
            "status": "active"
        }
        
        self.sessions.insert_one(doc)
        return session_id
    
    def update_session(
        self,
        session_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """Update session metadata.
        
        Args:
            session_id: Session identifier
            updates: Fields to update
            
        Returns:
            True if updated successfully
        """
        updates["updated_at"] = datetime.utcnow()
        result = self.sessions.update_one(
            {"session_id": session_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session document or None
        """
        return self.sessions.find_one({"session_id": session_id})
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()
        logger.info("🔒 MongoDB connection closed")
