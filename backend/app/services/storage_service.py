"""
Google Cloud Storage service for storing generated assets
"""
from google.cloud import storage
import base64
import logging
from datetime import datetime
import uuid
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class StorageService:
    """Service for managing Cloud Storage uploads"""

    def __init__(self):
        self.client = storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)
        self.bucket = self.client.bucket(settings.STORAGE_BUCKET_NAME)

    async def upload_image(
        self,
        image_url: str,
        session_id: str,
        content_type: str = "image/png"
    ) -> str:
        """
        Upload an image to Cloud Storage

        Args:
            image_url: Base64 encoded image or URL
            session_id: Story session ID
            content_type: MIME type of the image

        Returns:
            Public URL of the uploaded image
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"sessions/{session_id}/illustrations/{timestamp}_{unique_id}.png"

            # Decode base64 image
            if image_url.startswith("data:"):
                # Extract base64 data
                image_data = image_url.split(",")[1]
            else:
                image_data = image_url

            image_bytes = base64.b64decode(image_data)

            # Upload to Cloud Storage
            blob = self.bucket.blob(filename)
            blob.upload_from_string(image_bytes, content_type=content_type)

            # Make public
            blob.make_public()

            public_url = blob.public_url
            logger.info(f"Image uploaded: {public_url}")

            return public_url

        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            raise

    async def upload_audio(
        self,
        audio_data: bytes,
        session_id: str,
        content_type: str = "audio/wav"
    ) -> str:
        """Upload audio file to Cloud Storage"""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"sessions/{session_id}/audio/{timestamp}_{unique_id}.wav"

            blob = self.bucket.blob(filename)
            blob.upload_from_string(audio_data, content_type=content_type)
            blob.make_public()

            return blob.public_url

        except Exception as e:
            logger.error(f"Error uploading audio: {str(e)}")
            raise

    async def get_session_files(self, session_id: str) -> list:
        """Get all files for a session"""
        try:
            prefix = f"sessions/{session_id}/"
            blobs = self.bucket.list_blobs(prefix=prefix)

            files = []
            for blob in blobs:
                files.append({
                    "name": blob.name,
                    "url": blob.public_url,
                    "created": blob.time_created.isoformat() if blob.time_created else None,
                    "size": blob.size
                })

            return files

        except Exception as e:
            logger.error(f"Error getting session files: {str(e)}")
            return []

    async def delete_session_files(self, session_id: str) -> bool:
        """Delete all files for a session"""
        try:
            prefix = f"sessions/{session_id}/"
            blobs = self.bucket.list_blobs(prefix=prefix)

            for blob in blobs:
                blob.delete()

            logger.info(f"Deleted files for session {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting session files: {str(e)}")
            return False
