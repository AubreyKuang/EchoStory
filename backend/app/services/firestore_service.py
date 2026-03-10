"""
Firestore service for storing story sessions and journal entries
"""
from google.cloud import firestore
import logging
from datetime import datetime
from typing import Optional, List, Dict
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FirestoreService:
    """Service for managing Firestore operations"""

    def __init__(self):
        self.db = firestore.Client(project=settings.GOOGLE_CLOUD_PROJECT)
        self.collection = settings.FIRESTORE_COLLECTION

    async def save_session(self, session_id: str, session_data: Optional[dict] = None) -> dict:
        """Save or update a story session"""
        try:
            doc_ref = self.db.collection(self.collection).document(session_id)

            if session_data is None:
                # Initialize new session
                session_data = {
                    "session_id": session_id,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                    "story_segments": [],
                    "status": "active"
                }
            else:
                session_data["updated_at"] = firestore.SERVER_TIMESTAMP

            doc_ref.set(session_data, merge=True)
            logger.info(f"Session saved: {session_id}")

            return {"session_id": session_id, "status": "saved"}

        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            raise

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve a story session"""
        try:
            doc_ref = self.db.collection(self.collection).document(session_id)
            doc = doc_ref.get()

            if doc.exists:
                data = doc.to_dict()
                return data
            else:
                return None

        except Exception as e:
            logger.error(f"Error getting session: {str(e)}")
            raise

    async def save_segment(self, session_id: str, segment: dict):
        """Add a story segment to a session"""
        try:
            doc_ref = self.db.collection(self.collection).document(session_id)

            # Add timestamp to segment
            segment["timestamp"] = firestore.SERVER_TIMESTAMP

            # Use array union to add segment
            doc_ref.update({
                "story_segments": firestore.ArrayUnion([segment]),
                "updated_at": firestore.SERVER_TIMESTAMP
            })

            logger.info(f"Segment saved to session {session_id}")

        except Exception as e:
            logger.error(f"Error saving segment: {str(e)}")
            raise

    async def list_sessions(
        self,
        limit: int = 10,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[dict]:
        """List story sessions with pagination"""
        try:
            query = self.db.collection(self.collection)

            # Filter by status if provided
            if status:
                query = query.where("status", "==", status)

            # Order by created date (newest first)
            query = query.order_by("created_at", direction=firestore.Query.DESCENDING)

            # Pagination
            query = query.limit(limit).offset(offset)

            sessions = []
            for doc in query.stream():
                data = doc.to_dict()
                sessions.append(data)

            return sessions

        except Exception as e:
            logger.error(f"Error listing sessions: {str(e)}")
            raise

    async def update_session_status(self, session_id: str, status: str):
        """Update session status (active, completed, archived)"""
        try:
            doc_ref = self.db.collection(self.collection).document(session_id)
            doc_ref.update({
                "status": status,
                "updated_at": firestore.SERVER_TIMESTAMP
            })

            logger.info(f"Session {session_id} status updated to {status}")

        except Exception as e:
            logger.error(f"Error updating session status: {str(e)}")
            raise

    async def delete_session(self, session_id: str):
        """Delete a story session"""
        try:
            doc_ref = self.db.collection(self.collection).document(session_id)
            doc_ref.delete()

            logger.info(f"Session {session_id} deleted")

        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            raise

    async def get_session_statistics(self, session_id: str) -> dict:
        """Get statistics for a session"""
        try:
            session = await self.get_session(session_id)

            if not session:
                return {}

            segments = session.get("story_segments", [])

            return {
                "total_segments": len(segments),
                "total_illustrations": sum(1 for s in segments if s.get("illustration_url")),
                "emotions_detected": [s.get("emotion") for s in segments if s.get("emotion")],
                "duration": None  # Calculate from timestamps if needed
            }

        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
