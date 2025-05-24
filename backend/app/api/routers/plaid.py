from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from plaid.model import (
    LinkTokenCreateRequest, LinkTokenCreateRequestUser,
    Products, CountryCode, ItemPublicTokenExchangeRequest
)
from ...core.plaid_client import plaid_client
from ...core.config import settings

router = APIRouter(prefix="/plaid", tags=["plaid"])


# models
class UserSettings(BaseModel):
    client_user_id: str
    language: str
    phone_num: Optional[str] = None


class PublicTokenRequest(BaseModel):
    public_token: str


# endpoints 
@router.post("/link-token")
def create_link_token(user_settings: UserSettings):
    req = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id=user_settings.client_user_id,
            phone_number=user_settings.phone_num,
        ),
        client_name=settings.app_name,
        products=[Products("transactions")],
        country_codes=[CountryCode("US")],
        language=user_settings.language,
    )
    resp = plaid_client.link_token_create(req)
    
    return {"link_token": resp["link_token"]}


@router.post("/exchange-public-token")
def exchange_public_token(payload: PublicTokenRequest):
    req = ItemPublicTokenExchangeRequest(public_token=payload.public_token)
    resp = plaid_client.item_public_token_exchange(req)

    return {"item_id": resp["item_id"]}
