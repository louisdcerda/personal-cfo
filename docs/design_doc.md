**Design Document: Personal CFO App**

---

## 1. Overview

**Name:** Personal CFO
**Purpose:** An AI-powered financial assistant built for freelancers, creators, and small business owners to track income, manage expenses, save for taxes, and receive intelligent financial nudges.
**Primary Differentiator:** Combines real-time financial analysis, automated tax planning, and actionable insights in one platform tailored to the 1099/contractor lifestyle.

---

## 2. Target Users

* Freelancers, independent contractors, and gig workers
* Creators with income across multiple platforms (e.g. Stripe, PayPal, Patreon)
* Solo entrepreneurs running service-based businesses

---

## 3. Key Features

### 3.1 Account Linking

* Integrate with bank accounts and credit cards using Plaid
* Pull transactions and balances in real time

### 3.2 Smart Categorization

* Automatically label transactions as income, expenses, or transfers
* Distinguish between personal and business spending

### 3.3 Income Tracking & Profitability

* Track monthly/quarterly income
* Show gross vs. net income breakdown

### 3.4 Tax Estimator

* Estimate quarterly taxes owed based on income
* Suggest amounts to set aside in real time

### 3.5 Monthly Financial Report

* Show earnings, expenses, tax obligations, savings progress
* Provide plain-language insights and suggestions

### 3.6 AI Nudges

* Examples: "You received 3 payments this week. Time to save 30% for taxes."
* Identify high-spending categories and unused subscriptions
* Alert users when recurring charges change or are missed

### 3.7 Optional Add-ons (Phase 2+)

* Invoice creation and tracking
* Simple contractor payroll tool
* Business write-off tracker and optimizer
* Embedded savings account (via partner bank)

---

## 4. Technical Stack

**Frontend:** React (w/ Tailwind CSS), Vite, Plaid Link
**Backend:** FastAPI (Python), PostgreSQL, SQLAlchemy, Pydantic v2
**Auth:** JWT (access + session cookies), optional Google OAuth
**DevOps:** Docker Compose, GitHub Actions, Railway or AWS deployment

---

## 5. Architecture

* Microservices-based architecture using Docker
* Services:

  * `frontend`: UI served via Nginx
  * `backend`: API and business logic (FastAPI)
  * `worker`: Async job queue for syncing bank data, sending nudges
  * `db`: PostgreSQL for user data and transactions
  * `redis`: Job/message queue for async workers

---

## 6. Database Models (Simplified)

* `User`: id, email, password, created\_at, has\_linked\_bank
* `UserSession`: id, user\_id, ip, device, session\_token
* `BankAccount`: id, user\_id, name, institution
* `Transaction`: id, bank\_account\_id, date, amount, category, is\_business\_expense
* `Budget`: id, user\_id, target, category, amount
* `FinancialReport`: id, user\_id, month, income, expenses, tax\_suggestion

---

## 7. MVP Milestones

**Week 1-2:** User auth + bank account linking
**Week 3:** Transaction syncing + categorization logic
**Week 4:** Dashboard UI with income/spending summaries
**Week 5:** Tax estimation + monthly summary report
**Week 6:** AI nudges + notification system
**Week 7:** Soft launch with friends/testers
**Week 8+:** Iterate based on feedback, begin marketing site

---

## 8. Long-Term Vision

* Serve as the go-to financial tool for self-employed professionals
* Offer embedded financial services (e.g. savings vaults, tax payments)
* Integrate with Stripe/QuickBooks for deeper income analytics
* Possibly evolve into a vertical neo-bank for solopreneurs

---

## 9. Open Questions

* Should we allow users to manually tag transactions?
* Should reports be exportable as PDFs?
* Will we support multiple users per account in the future (e.g. partners)?
* What bank partner (e.g. Unit, Synapse) should we use if offering embedded finance?

---

## 10. Success Metrics

* % of users who link a bank in first session
* Weekly active users (WAU)
* Monthly retention rate
* % of users who use tax-saving recommendation
* % of nudges converted to user action
