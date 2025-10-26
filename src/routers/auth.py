from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
import secrets
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from App.Utility.config import oauth_settings
from App.Utility.session_manager import set_session_data, clear_session_data, get_session_data

router = APIRouter()

# --- GET /Auth/login ---
@router.get("/login")
async def login(request: Request, response: Response):
    state = secrets.token_hex(8)
    response.set_cookie(key="oauth_state", value=state, httponly=True, secure=True)

    params = {
        'client_id': oauth_settings.client_id,
        'redirect_uri': oauth_settings.redirect_uri,
        'response_type': 'code',
        'scope': 'public',
        'state': state
    }

    url = f"{oauth_settings.authorize_url}?{httpx.QueryParams(params).url_encoded}"
    return RedirectResponse(url=url, status_code=302)

# --- GET /Auth/callback ---
@router.get("/callback")
async def callback(request: Request, response: Response):
    code = request.query_params.get('code')
    state_from_url = request.query_params.get('state')
    state_from_cookie = request.cookies.get('oauth_state')

    response.delete_cookie(key="oauth_state")

    if not code or state_from_url != state_from_cookie:
        raise HTTPException(status_code=400, detail="Invalid or missing code/state.")

    # Заглушка: получение токена и user_info
    access_token = "dummy_access_token"
    user_info = {"id": 123, "login": "demo_user"}

    session_data = {
        'user_password': 'verified',
        'access_token': access_token,
        'user_info': user_info,
        'first_login_date': datetime.now(timezone.utc).isoformat()
    }
    await set_session_data(response, session_data)
    return RedirectResponse(url="/dashboard", status_code=302)

# --- GET /Auth/logout ---
@router.get("/logout")
async def logout(response: Response):
    await clear_session_data(response)
    return RedirectResponse(url="/", status_code=302)
