from plaid import Configuration, ApiClient
from plaid.api import plaid_api
from plaid.exceptions import ApiException
from .config import settings
from fastapi import HTTPException, status

def get_plaid_client() -> plaid_api.PlaidApi:
    host_map = {
        "sandbox": "https://sandbox.plaid.com",
        "development": "https://development.plaid.com",
        "production": "https://production.plaid.com",
    }
    
    if settings.plaid_env not in host_map:
        raise ValueError(f"Invalid Plaid environment: {settings.plaid_env}")
    
    configuration = Configuration(
        host=host_map[settings.plaid_env],
        api_key={
            "clientId": settings.plaid_client_id,
            "secret": settings.plaid_secret,
            "plaidVersion": "2020-09-14",
        },
    )
    
    return plaid_api.PlaidApi(ApiClient(configuration))

def handle_plaid_error(e: ApiException) -> None:
    """Handle Plaid API errors and convert them to appropriate HTTP exceptions"""
    if e.status == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request to Plaid: {str(e)}"
        )
    elif e.status == 401:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Plaid credentials"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Plaid service error: {str(e)}"
        )

# Optional: create one global so you don't rebuild it every request
plaid_client = get_plaid_client()
