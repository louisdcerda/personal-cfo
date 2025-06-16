from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import os

from plaid import Configuration, ApiClient
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from app.deps import get_db
from app.core.auth import get_current_user
from app.models import User, PlaidItem

try:
    from ...core.config import settings
    PLAID_CLIENT_ID = settings.plaid_client_id
    PLAID_SECRET = settings.plaid_secret
    PLAID_ENV = settings.plaid_env
    APP_NAME = settings.app_name
except ImportError:
    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET = os.getenv("PLAID_SECRET", "")
    PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
    APP_NAME = os.getenv("APP_NAME", "Personal CFO")

_HOSTS = {
    "sandbox": "https://sandbox.plaid.com",
    "development": "https://development.plaid.com",
    "production": "https://production.plaid.com",
}
configuration = Configuration(
    host=_HOSTS.get(PLAID_ENV, _HOSTS["sandbox"]),
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "plaidVersion": "2020-09-14",
    },
)
plaid_client = plaid_api.PlaidApi(ApiClient(configuration))

router = APIRouter(prefix="/plaid", tags=["plaid"])

# ----------------- Models -------------------

class UserSettings(BaseModel):
    client_user_id: str
    language: str
    phone_num: Optional[str] = None

    model_config = {"from_attributes": True}


class PublicTokenRequest(BaseModel):
    public_token: str


# ----------------- Routes -------------------

@router.post("/link-token")
def create_link_token(user_settings: UserSettings):
    """Generate a Plaid Link token."""
    req = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id=user_settings.client_user_id,
            phone_number=user_settings.phone_num,
        ),
        client_name=APP_NAME,
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language=user_settings.language,
    )

    try:
        resp = plaid_client.link_token_create(req)
        return {"link_token": resp.link_token}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Plaid link_token_create failed: {e}",
        ) from e


@router.post("/exchange-public-token")
def exchange_public_token(
    payload: PublicTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Exchange a public_token for an access_token and item_id."""
    req = ItemPublicTokenExchangeRequest(public_token=payload.public_token)

    try:
        resp = plaid_client.item_public_token_exchange(req)

        plaid_item = PlaidItem(
            user_id=current_user.id,
            access_token=resp.access_token,
            item_id=resp.item_id
        )
        db.add(plaid_item)

        current_user.bank_linked = True  # make sure this column exists
        db.commit()

        return {"item_id": resp.item_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Plaid item_public_token_exchange failed: {e}",
        ) from e
