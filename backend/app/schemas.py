from pydantic import BaseModel, EmailStr
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    category: str | None = None
    date: datetime

class TransactionCreate(TransactionBase):
    plaid_txn_id: str
    iso_currency_code: str

class Transaction(TransactionBase):
    id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None

class User(UserCreate):
    id: int
    class Config:
        orm_mode = True
