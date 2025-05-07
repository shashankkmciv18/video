import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Request


class AuthCallbackController:
    def __init__(self):
        load_dotenv()
        self.router = APIRouter()
        self.APP_ID = os.getenv("APP_ID")
        self.APP_SECRET = os.getenv("APP_SECRET")
        self.REDIRECT_URI = os.getenv("REDIRECT_HOST")+os.getenv("REDIRECT_URI")
        self.router.add_api_route("/auth/callback", self.auth_callback, methods=["GET"])

    def auth_callback(self, request: Request):
        code = request.query_params.get("code")
        if not code:
            return {"error": "Missing authorization code from Facebook"}

        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "client_id": self.APP_ID,
            "client_secret": self.APP_SECRET,
            "redirect_uri": self.REDIRECT_URI,
            "code": code,
        }

        token_res = requests.get(token_url, params=params)
        if token_res.status_code != 200:
            return {"error": "Failed to fetch access token", "details": token_res.text}

        access_token = token_res.json().get("access_token")
        return {
            "message": "Short-lived access token retrieved successfully",
            "access_token": access_token,
        }


# Instantiate the controller and use its router
auth_callback_controller = AuthCallbackController()
router = auth_callback_controller.router
