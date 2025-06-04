from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime


#
# 1) AUTH / USER SCHEMAS
#
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str   # Plain‐text in schema; hash on server side


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AuthTokenBase(BaseModel):
    token: str
    expires_at: datetime


class AuthTokenRead(AuthTokenBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


#
# 2) OAUTH / SOCIAL LOGIN
#
class OAuthAccountBase(BaseModel):
    provider_name: str
    provider_user_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class OAuthAccountCreate(OAuthAccountBase):
    pass


class OAuthAccountRead(OAuthAccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


#
# 3) USER SETTINGS
#
class UserSettingBase(BaseModel):
    key: str
    value: Dict[str, Any]   # store any JSON‐serializable object


class UserSettingCreate(UserSettingBase):
    pass


class UserSettingRead(UserSettingBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


#
# 4) BANK ACCOUNT (PLAID) + TRANSACTIONS
#
class BankAccountBase(BaseModel):
    plaid_account_id: str
    institution_name: Optional[str] = None
    name: Optional[str] = None
    mask: Optional[str] = None
    official_name: Optional[str] = None
    type: Optional[str] = None
    subtype: Optional[str] = None
    iso_currency_code: Optional[str] = None
    available_balance: Optional[float] = None
    current_balance: Optional[float] = None
    raw_account_data: Optional[Dict[str, Any]] = None


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountRead(BankAccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float
    category: Optional[List[str]] = None
    transaction_date: datetime
    merchant_name: Optional[str] = None
    pending: bool


class TransactionCreate(TransactionBase):
    plaid_transaction_id: str
    iso_currency_code: str
    raw_transaction_data: Optional[Dict[str, Any]] = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int
    bank_account_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


#
# 5) CATEGORIES & BUDGETS
#
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class BudgetBase(BaseModel):
    name: str
    period_start: datetime
    period_end: datetime
    total_amount: float


class BudgetCreate(BudgetBase):
    pass


class BudgetRead(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    items: List["BudgetItemRead"] = []  # forward reference

    class Config:
        orm_mode = True


class BudgetItemBase(BaseModel):
    category_id: int
    allocated_amount: float


class BudgetItemCreate(BudgetItemBase):
    pass


class BudgetItemRead(BudgetItemBase):
    id: int
    budget_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


BudgetRead.update_forward_refs()


#
# 6) INVESTMENTS
#
class InvestmentAccountBase(BaseModel):
    broker_name: str
    account_mask: Optional[str] = None
    account_type: Optional[str] = None
    raw_account_data: Optional[Dict[str, Any]] = None


class InvestmentAccountCreate(InvestmentAccountBase):
    pass


class InvestmentAccountRead(InvestmentAccountBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    holdings: List["InvestmentHoldingRead"] = []

    class Config:
        orm_mode = True


class InvestmentHoldingBase(BaseModel):
    symbol: str
    quantity: float
    cost_basis: Optional[float] = None
    market_value: Optional[float] = None
    last_price: Optional[float] = None
    last_updated: datetime


class InvestmentHoldingCreate(InvestmentHoldingBase):
    pass


class InvestmentHoldingRead(InvestmentHoldingBase):
    id: int
    investment_account_id: int
    raw_holding_data: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True


InvestmentAccountRead.update_forward_refs()


#
# 7) FINANCIAL REPORTS
#
class FinancialReportBase(BaseModel):
    period_start: datetime
    period_end: datetime
    total_income: Optional[float] = None
    total_expenses: Optional[float] = None
    net_savings: Optional[float] = None
    report_data: Optional[Dict[str, Any]] = None


class FinancialReportCreate(FinancialReportBase):
    pass


class FinancialReportRead(FinancialReportBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


#
# 8) PASSWORD RESETS
#
class PasswordResetBase(BaseModel):
    expires_at: datetime


class PasswordResetCreate(PasswordResetBase):
    pass


class PasswordResetRead(PasswordResetBase):
    id: int
    user_id: int
    reset_token: str
    created_at: datetime

    class Config:
        orm_mode = True


#
# 9) AUDIT LOGS
#
class AuditLogBase(BaseModel):
    event_type: str
    event_details: Optional[Dict[str, Any]] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


#
# 10) USER SESSIONS
#
class UserSessionBase(BaseModel):
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime


class UserSessionCreate(UserSessionBase):
    session_token: str


class UserSessionRead(UserSessionBase):
    id: int
    user_id: int
    created_at: datetime
    last_active_at: datetime

    class Config:
        orm_mode = True
