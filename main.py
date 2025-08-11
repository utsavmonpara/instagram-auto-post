from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from instagram_client import InstagramClient

app = FastAPI(title="Instagram Auto Post", version="1.0.0")

# Initialize Instagram client
instagram_client = InstagramClient()

class PostRequest(BaseModel):
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    caption: str
    scheduled_time: Optional[str] = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Instagram Auto Post",
        "version": "1.0.0"
    }

@app.post("/schedule")
async def schedule_post(post_request: PostRequest):
    """Schedule a post to Instagram"""
    try:
        if post_request.image_url:
            # Post image
            result = await instagram_client.post_image(
                image_url=post_request.image_url,
                caption=post_request.caption,
                scheduled_time=post_request.scheduled_time
            )
        elif post_request.video_url:
            # Post reel/video
            result = await instagram_client.post_reel(
                video_url=post_request.video_url,
                caption=post_request.caption,
                scheduled_time=post_request.scheduled_time
            )
        else:
            raise HTTPException(status_code=400, detail="Either image_url or video_url must be provided")
        
        return {
            "status": "success",
            "message": "Post scheduled successfully",
            "post_id": result.get("id"),
            "scheduled_time": post_request.scheduled_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule post: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Instagram Auto Post API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
