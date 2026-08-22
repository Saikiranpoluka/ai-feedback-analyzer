# 🤖 AI Feedback Analyzer

> A Python-based LLM pipeline that transforms unstructured customer feedback into structured sentiment, themes, and categories, then persists the results in MySQL for downstream analysis.

## 📌 Overview

Customer feedback often arrives as free-form text that is difficult to analyze consistently at scale. This project demonstrates an AI-assisted workflow that converts unstructured feedback into structured information that can be queried and used for reporting.

The core pipeline sends feedback to an LLM, extracts structured insights, and stores the resulting records in MySQL.

## 🧩 End-to-End Workflow

```text
Raw Customer Feedback
        ↓
Input Validation
        ↓
LLM Analysis
        ↓
Structured Insights
 ┌────────┬───────────┬────────────┐
 │Sentiment│   Theme   │  Category  │
 └────────┴───────────┴────────────┘
        ↓
Validation / Transformation
        ↓
MySQL Storage
        ↓
SQL Analytics / Reporting
```

## ✨ Key Capabilities

- **LLM-powered analysis:** Uses the OpenAI API to interpret unstructured feedback.
- **Structured extraction:** Converts free-form text into fields such as sentiment, theme, and category.
- **Persistent storage:** Stores analyzed feedback in MySQL for querying and downstream analytics.
- **Environment-based configuration:** Keeps API keys and database credentials outside source control.
- **Containerized development:** Includes Dev Container configuration for a consistent development environment.

## 🧪 Example

### Input

```text
"The product quality is good, but delivery took too long and support did not respond quickly."
```

### Structured output

```text
Sentiment: Negative / Mixed
Theme: Delivery & Support
Category: Customer Experience
```

> The exact output depends on the configured model and prompt/schema.

## 🛠️ Tech Stack

- **Language:** Python
- **AI / NLP:** OpenAI API, Transformers, PyTorch
- **Database:** MySQL
- **Application:** Streamlit / Python application workflow
- **Environment:** Virtual environments, VS Code Dev Containers

## 📂 Project Structure

```text
ai-feedback-analyzer/
├── .devcontainer/
├── ai_pipeline.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Run Locally

### Prerequisites

- Python 3.10+
- MySQL Server
- OpenAI API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Saikiranpoluka/ai-feedback-analyzer.git
cd ai-feedback-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file and keep it out of Git:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_secure_password
DB_NAME=feedback_db
OPENAI_API_KEY=your_openai_api_key
```

Create the required MySQL database before running the application.

### 5. Run

```bash
python app.py
```

If the application entry point changes, follow the execution instructions defined in `app.py`.

## 🔐 Security

- Never commit `.env` files or API keys.
- Never hard-code database passwords or credentials.
- Rotate credentials immediately if they are accidentally exposed.
- Treat customer feedback as potentially sensitive data and avoid using real personally identifiable information in development datasets.

## 🧠 Engineering Highlights

- Demonstrates an end-to-end **unstructured text → LLM → structured data → SQL** workflow.
- Separates the AI-processing logic from the application entry point.
- Uses persistent relational storage instead of keeping results only in memory.
- Provides a foundation for integrating LLM outputs with traditional analytics systems.

## 🔮 Future Improvements

- Enforce a strict structured-output schema using JSON validation or Pydantic.
- Add retries, timeout handling, and graceful API-error handling.
- Add automated tests for parsing, validation, and database operations.
- Add batch processing for large feedback datasets.
- Add prompt/version tracking and model evaluation.
- Add token/cost tracking and latency monitoring.
- Add a FastAPI endpoint for external systems.
- Add a Power BI dashboard over the analyzed MySQL data.
- Add anonymization/PII detection before sending feedback to an external model.

## ⚠️ Limitations

LLM-generated classifications can contain errors or inconsistent outputs. Production usage should include schema validation, confidence/quality checks, human review for sensitive cases, prompt and model evaluation, privacy controls, and monitoring.

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
