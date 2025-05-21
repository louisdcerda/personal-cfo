# Spending-Coach 🚀
AI-powered, real-time budgeting for busy people.

> **One-liner**  
> “Connect your bank in 30 seconds and get a daily chat message that tells you exactly what to adjust to stay on budget.”

---

## ✨ Features (MVP v0)
* 🔌 **Secure account aggregation** — Plaid sandbox today, open-banking in prod  
* 📊 **Auto-categorized spend feed** — enriched with ML embeddings  
* 🤖 **LLM spending coach** — rewrites cold numbers into friendly, actionable nudges  
* 📱 **Daily SMS / in-app push** — zero-friction habit loop

---

## 🏗️ Architecture
```mermaid
graph TD
    subgraph Containers
        A[FastAPI (api)] -->|SQLAlchemy| C[(Postgres)]
        B[Worker (schedule)] -->|SQLAlchemy| C
        B -->|Plaid API| D[Plaid]
        B -->|OpenAI| E[LLM]
        B -->|Twilio| F[SMS]
    end
    click A href "http://localhost:8000/docs" "Swagger UI"

