from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests

class PushNotificationInput(BaseModel):
    """A message to be sent to the user."""
    message: str = Field(..., description="The message to BE sent to the user.")

class PushNotificationTool(BaseTool):
    name: str = "Send Push Notification"
    description: str = (
        "This tool sends a push notification to the user with the provided message. "
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"push: {message}")
        payload = {
            "token": pushover_token,
            "user": pushover_user,
            "message": message
        }
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'
