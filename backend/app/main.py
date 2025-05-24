# plaid imports 
import plaid
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.api import plaid_api

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, crud, schemas
from pydantic import BaseModel
from typing import Optional
import os



app = FastAPI(title="Personal CFO API")



client_id = os.getenv('PLAID_CLIENT_ID')
plaid_secret = os.getenv('PLAID_SECRET')
application_name = "PERSONAL_CFO"



configuration = plaid.Configuration(
    host="https://sandbox.plaid.com",    
    api_key={
        'clientId': client_id,
        'secret': plaid_secret,
        'plaidVersion': '2020-09-14'
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)






class UserSettings(BaseModel):
    client_user_id: str
    language: str
    phone_num: Optional[str] = None

    model_config = {
        "from-attributes": True
    }

# the link token gets passes to the client 
@app.post("/link-token")
def create_link_token(user_settings: UserSettings):
    # hit create link token on plain

    # Account filtering isn't required here, but sometimes 
    # it's helpful to see an example. 

    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id= user_settings.client_user_id,
            phone_number= user_settings.phone_num
        ),
        client_name=application_name,
        products=[Products('transactions')],
        country_codes=[CountryCode('US')],
        language= user_settings.language,

    )

    # create link token
    response = client.link_token_create(request)
    print(response)
    link_token = response['link_token']

    return link_token


# exchange the link token for an access token
# in prod change this to db for the user requesting
access_token = None
item_id = None

class PublicTokenRequest(BaseModel):
    public_token: str


@app.post("/exchange-public-token")
def exchange_public_token(payload: PublicTokenRequest):
    global access_token, item_id 


    public_token = payload.public_token
    request = ItemPublicTokenExchangeRequest(
      public_token=public_token
    )
    response = client.item_public_token_exchange(request)

    access_token = response['access_token']
    item_id = response['item_id']

    return "success"