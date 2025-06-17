# Personal CFO

AI-powered, real-time budgeting for busy people.

> **One-liner**  
> “Connect your bank in 30 seconds and get a daily chat message that tells you exactly what to adjust to stay on budget.”

---

## Features (MVP v0)

- **Secure account aggregation** — Plaid Sandbox integration for development, open banking support planned for production  
- **Auto-categorized spend feed** — transactions enriched using machine learning embeddings  
- **LLM spending coach** — translates raw financial data into actionable, conversational nudges  
- **Daily SMS / in-app push notifications** — enables a frictionless budgeting habit loop

---

## Architecture

```mermaid
graph TD
    subgraph Containers
        A[FastAPI (API)] -->|SQLAlchemy| C[(PostgreSQL)]
        B[Worker (Scheduler)] -->|SQLAlchemy| C
        B -->|Plaid API| D[Plaid]
        B -->|OpenAI API| E[LLM]
        B -->|Twilio API| F[SMS]
    end
    click A href "http://localhost:8000/docs" "Swagger UI"
