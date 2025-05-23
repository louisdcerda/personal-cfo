from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import database, crud, schemas
from typing import Optional
import os

app = FastAPI(title="Personal CFO API")
client_id = os.getenv['PLAID_CLIENT_ID']
plaid_secret = os.getenv['PLAID_SECRET']
application_name = "PERSONAL_CFO"


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

@app.get("/link-token")
def create_link_token(client_user_id: str, user_settings: user_settings):
    # passing in a user settings object so have to parse it 
    lang = user_settings['language']
    phone_num = user_settings['phone_num']


    # hit create link token on plain

    # Account filtering isn't required here, but sometimes 
    # it's helpful to see an example. 

    request = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(
            client_user_id=client_user_id,
            phone_number=phone_num
        ),
        client_name=application_name,
        products=[Products('transactions')],
        transactions=LinkTokenTransactions(
            days_requested=730
        ),
        country_codes=[CountryCode('US')],
        language=lang,
        webhook='https://sample-web-hook.com',
        redirect_uri='https://domainname.com/oauth-page.html',
    )

    # create link token
    response = client.link_token_create(request)
    link_token = response['link_token']

    return link_token