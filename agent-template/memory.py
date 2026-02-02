"""MongoDB memory management for agents."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class MongoMemory:
    """MongoDB-based memory for agent interactions."""
    
    def __init__(self, uri: str = "mongodb://admin:admin123@localhost:27017/"):
        """Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI
        """
        self.client = MongoClient(uri)
        self.db = self.client.agent_memory
        self.interactions: Collection = self.db.interactions
        self.sessions: Collection = self.db.sessions
        
        # Create indexes for efficient queries (ignore if already exists)
        try:
            self.interactions.create_index([("session_id", ASCENDING), ("timestamp", ASCENDING)])
        except Exception:
            pass  # Index already exists
        
        try:
            self.sessions.create_index("session_id", unique=True)
        except Exception:
            pass  # Index already exists
        
        logger.info("✅ MongoDB memory initialized")
    
    def save_interaction(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Save an interaction to memory.
        
        Args:
            session_id: Session identifier
            role: Role (user, assistant, system)
            content: Message content
            metadata: Additional metadata
            
        Returns:
            Interaction ID
        """
        interaction = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow()
        }
        
        result = self.interactions.insert_one(interaction)
        logger.debug(f"💾 Saved interaction for session {session_id}")
        
        return str(result.inserted_id)
    
    def get_session_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get interaction history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of interactions
            
        Returns:
            List of interactions
        """
        interactions = self.interactions.find(
            {"session_id": session_id}
        ).sort("timestamp", ASCENDING).limit(limit)
        
        history = []
        for interaction in interactions:
            history.append({
                "role": interaction["role"],
                "content": interaction["content"],
                "timestamp": interaction["timestamp"],
                "metadata": interaction.get("metadata", {})
            })
        
        logger.debug(f"📖 Retrieved {len(history)} interactions for session {session_id}")
        return history
    
    def create_session(
        self,
        session_id: str,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Create a new session.
        
        Args:
            session_id: Session identifier
            metadata: Session metadata
            
        Returns:
            True if created, False if exists
        """
        try:
            session = {
                "session_id": session_id,
                "metadata": metadata or {},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            self.sessions.insert_one(session)
            logger.info(f"✅ Created session {session_id}")
            return True
            
        except Exception as e:
            logger.warning(f"Session {session_id} already exists")
            return False
    
    def update_session(
        self,
        session_id: str,
        metadata: Dict[str, Any]
    ):
        """Update session metadata.
        
        Args:
            session_id: Session identifier
            metadata: Metadata to update
        """
        self.sessions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "metadata": metadata,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        logger.debug(f"📝 Updated session {session_id}")
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session document or None
        """
        return self.sessions.find_one({"session_id": session_id})
    
    def delete_session(self, session_id: str):
        """Delete a session and all its interactions.
        
        Args:
            session_id: Session identifier
        """
        self.interactions.delete_many({"session_id": session_id})
        self.sessions.delete_one({"session_id": session_id})
        logger.info(f"🗑️ Deleted session {session_id}")
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()
        logger.info("🔌 MongoDB connection closed")
