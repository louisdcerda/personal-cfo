from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Text,
    Numeric,
    JSON,
    ARRAY,
    UniqueConstraint,
    Index
)
from sqlalchemy.dialects.postgresql import JSONB, INET
from sqlalchemy.orm import relationship
from .database import Base


def now():
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=now, onupdate=now, nullable=False
    )

    # Relationships
    auth_tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    oauth_accounts = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    user_settings = relationship("UserSetting", back_populates="user", cascade="all, delete-orphan")
    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    investment_accounts = relationship("InvestmentAccount", back_populates="user", cascade="all, delete-orphan")
    financial_reports = relationship("FinancialReport", back_populates="user", cascade="all, delete-orphan")
    password_resets = relationship("PasswordReset", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    user_sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    has_linked_bank = Column(Boolean, default=False, nullable=False)


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(512), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

    user = relationship("User", back_populates="auth_tokens")


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        UniqueConstraint("provider_name", "provider_user_id", name="ux_oauth_provider_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider_name = Column(String(50), nullable=False)       # e.g. 'google', 'facebook'
    provider_user_id = Column(String(255), nullable=False)    # provider's unique user ID
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="oauth_accounts")


class UserSetting(Base):
    __tablename__ = "user_settings"
    __table_args__ = (
        UniqueConstraint("user_id", "key", name="ux_user_settings_user_key"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(100), nullable=False)                 # e.g. 'theme', 'currency'
    value = Column(JSONB, nullable=False)                     # e.g. {"theme":"light"}
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="user_settings")


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "plaid_account_id", name="ux_bank_account_user_plaid"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plaid_account_id = Column(String(100), nullable=False)    # Plaid’s “account_id”
    institution_name = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)                 # e.g. “Chase Checking”
    mask = Column(String(20), nullable=True)                  # last 4 digits
    official_name = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)                  # e.g. “depository”, “credit”
    subtype = Column(String(50), nullable=True)               # e.g. “checking”, “savings”
    iso_currency_code = Column(String(10), nullable=True)
    available_balance = Column(Numeric(14, 2), nullable=True)
    current_balance = Column(Numeric(14, 2), nullable=True)
    raw_account_data = Column(JSONB, nullable=True)            # store full Plaid response if desired
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="bank_accounts")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=False)
    plaid_transaction_id = Column(String(100), unique=True, index=True, nullable=False)  # Plaid’s “transaction_id”
    name = Column(Text, nullable=True)                                                     # e.g. merchant name
    amount = Column(Numeric(14, 2), nullable=False)
    iso_currency_code = Column(String(10), nullable=True)
    transaction_date = Column(DateTime(timezone=False), nullable=False)
    merchant_name = Column(String(255), nullable=True)
    category = Column(ARRAY(String), nullable=True)                                        # e.g. ['Food', 'Restaurants']
    pending = Column(Boolean, default=False, nullable=False)
    raw_transaction_data = Column(JSONB, nullable=True)                                    # full JSON blob from Plaid
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    bank_account = relationship("BankAccount", back_populates="transactions")
    user = relationship("User")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="ux_category_user_name"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)       # e.g. “Groceries”, “Utilities”
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="subcategories")


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "period_start", "period_end", name="ux_budget_user_period"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)        # e.g. “June 2025 Budget”
    period_start = Column(DateTime(timezone=False), nullable=False)
    period_end = Column(DateTime(timezone=False), nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="budgets")
    items = relationship("BudgetItem", back_populates="budget", cascade="all, delete-orphan")


class BudgetItem(Base):
    __tablename__ = "budget_items"
    __table_args__ = (
        UniqueConstraint("budget_id", "category_id", name="ux_budget_item_budget_category"),
    )

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    allocated_amount = Column(Numeric(14, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    budget = relationship("Budget", back_populates="items")
    category = relationship("Category")


class InvestmentAccount(Base):
    __tablename__ = "investment_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    broker_name = Column(String(150), nullable=False)       # e.g. “Robinhood”
    account_mask = Column(String(50), nullable=True)        # e.g. “****1234”
    account_type = Column(String(50), nullable=True)        # e.g. “brokerage”
    raw_account_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)

    user = relationship("User", back_populates="investment_accounts")
    holdings = relationship("InvestmentHolding", back_populates="account", cascade="all, delete-orphan")


class InvestmentHolding(Base):
    __tablename__ = "investment_holdings"
    __table_args__ = (
        UniqueConstraint("investment_account_id", "symbol", name="ux_invest_holding_account_symbol"),
    )

    id = Column(Integer, primary_key=True, index=True)
    investment_account_id = Column(Integer, ForeignKey("investment_accounts.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String(20), nullable=False)                    # e.g. “AAPL”
    quantity = Column(Numeric(20, 8), nullable=False)               # fractional shares
    cost_basis = Column(Numeric(20, 4), nullable=True)
    market_value = Column(Numeric(20, 4), nullable=True)
    last_price = Column(Numeric(20, 4), nullable=True)
    last_updated = Column(DateTime(timezone=True), default=now, nullable=False)
    raw_holding_data = Column(JSONB, nullable=True)

    account = relationship("InvestmentAccount", back_populates="holdings")


class FinancialReport(Base):
    __tablename__ = "financial_reports"
    __table_args__ = (
        UniqueConstraint("user_id", "period_start", "period_end", name="ux_report_user_period"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(DateTime(timezone=False), nullable=False)
    period_end = Column(DateTime(timezone=False), nullable=False)
    total_income = Column(Numeric(14, 2), nullable=True)
    total_expenses = Column(Numeric(14, 2), nullable=True)
    net_savings = Column(Numeric(14, 2), nullable=True)
    report_data = Column(JSONB, nullable=True)              # full breakdown JSON
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

    user = relationship("User", back_populates="financial_reports")


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reset_token = Column(String(512), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

    user = relationship("User", back_populates="password_resets")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_event_type", "event_type"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    event_type = Column(String(100), nullable=False)    # e.g. “USER_SIGNUP”
    event_details = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

    user = relationship("User", back_populates="audit_logs")


class PlaidItem(Base):
    __tablename__ = "plaid_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    access_token = Column(String(512), nullable=False)
    item_id = Column(String(255), nullable=False)
    institution_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    
    user = relationship("User", backref="plaid_items")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_token = Column(String(512), unique=True, nullable=False)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(INET, nullable=True)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    last_active_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="user_sessions")
