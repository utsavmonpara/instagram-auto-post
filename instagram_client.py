import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstagramClient:
    """Instagram Graph API client for posting images and reels"""
    
    def __init__(self):
        self.app_id = os.getenv("IG_APP_ID")
        self.app_secret = os.getenv("IG_APP_SECRET")
        self.user_id = os.getenv("IG_USER_ID")
        self.access_token = os.getenv("IG_ACCESS_TOKEN")
        self.page_id = os.getenv("IG_PAGE_ID")
        self.base_url = "https://graph.facebook.com/v18.0"
        
        # Validate required environment variables
        required_vars = ["IG_APP_ID", "IG_APP_SECRET", "IG_USER_ID", "IG_ACCESS_TOKEN", "IG_PAGE_ID"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
    
    async def post_image(self, image_url: str, caption: str, scheduled_time: Optional[str] = None) -> Dict[str, Any]:
        """Post an image to Instagram using Facebook Graph API
        
        Args:
            image_url (str): URL of the image to post
            caption (str): Caption for the post
            scheduled_time (str, optional): Scheduled time for the post (ISO format)
            
        Returns:
            Dict[str, Any]: Response from Instagram API
        """
        try:
            # Step 1: Create media container
            media_data = {
                "image_url": image_url,
                "caption": caption,
                "access_token": self.access_token
            }
            
            if scheduled_time:
                # Convert to Unix timestamp if scheduled
                scheduled_timestamp = int(datetime.fromisoformat(scheduled_time.replace('Z', '+00:00')).timestamp())
                media_data["published"] = "false"
                media_data["scheduled_publish_time"] = scheduled_timestamp
            
            # Create container
            container_url = f"{self.base_url}/{self.user_id}/media"
            container_response = requests.post(container_url, data=media_data)
            container_response.raise_for_status()
            
            container_id = container_response.json().get("id")
            
            if not scheduled_time:
                # Step 2: Publish immediately if not scheduled
                publish_data = {
                    "creation_id": container_id,
                    "access_token": self.access_token
                }
                
                publish_url = f"{self.base_url}/{self.user_id}/media_publish"
                publish_response = requests.post(publish_url, data=publish_data)
                publish_response.raise_for_status()
                
                return publish_response.json()
            else:
                return {"id": container_id, "status": "scheduled"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting image: {str(e)}")
            raise Exception(f"Failed to post image: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    async def post_reel(self, video_url: str, caption: str, scheduled_time: Optional[str] = None) -> Dict[str, Any]:
        """Post a reel/video to Instagram using Facebook Graph API
        
        Args:
            video_url (str): URL of the video to post
            caption (str): Caption for the reel
            scheduled_time (str, optional): Scheduled time for the post (ISO format)
            
        Returns:
            Dict[str, Any]: Response from Instagram API
        """
        try:
            # Step 1: Create reel container
            media_data = {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "access_token": self.access_token
            }
            
            if scheduled_time:
                # Convert to Unix timestamp if scheduled
                scheduled_timestamp = int(datetime.fromisoformat(scheduled_time.replace('Z', '+00:00')).timestamp())
                media_data["published"] = "false"
                media_data["scheduled_publish_time"] = scheduled_timestamp
            
            # Create container
            container_url = f"{self.base_url}/{self.user_id}/media"
            container_response = requests.post(container_url, data=media_data)
            container_response.raise_for_status()
            
            container_id = container_response.json().get("id")
            
            if not scheduled_time:
                # Step 2: Publish immediately if not scheduled
                publish_data = {
                    "creation_id": container_id,
                    "access_token": self.access_token
                }
                
                publish_url = f"{self.base_url}/{self.user_id}/media_publish"
                publish_response = requests.post(publish_url, data=publish_data)
                publish_response.raise_for_status()
                
                return publish_response.json()
            else:
                return {"id": container_id, "status": "scheduled"}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting reel: {str(e)}")
            raise Exception(f"Failed to post reel: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    def validate_access_token(self) -> bool:
        """Validate the Instagram access token
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            url = f"{self.base_url}/me"
            params = {"access_token": self.access_token}
            
            response = requests.get(url, params=params)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            return False
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get Instagram user information
        
        Returns:
            Dict[str, Any]: User information from Instagram API
        """
        try:
            url = f"{self.base_url}/{self.user_id}"
            params = {
                "fields": "id,username,account_type,media_count",
                "access_token": self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            raise Exception(f"Failed to get user info: {str(e)}")
