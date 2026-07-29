# AI Feedback Analyzer 🧠📊

An intelligent, Python-based application designed to process, analyze, and categorize feedback data using the power of Large Language Models (LLMs). By leveraging the OpenAI API and robust data storage solutions, this tool transforms raw text feedback into structured, actionable insights.

---

## 📖 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development Workflow](#development-workflow)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Handling large volumes of textual feedback (customer reviews, internal surveys, product feedback) can be overwhelming. The **AI Feedback Analyzer** automates this process by passing textual data through an AI pipeline. It extracts sentiment, identifies key themes, assigns appropriate categories, and securely logs the structured data into a MySQL database for downstream reporting and analytics. 

## ✨ Key Features

* **Advanced AI Processing (`ai_pipeline.py`)**: Utilizes the OpenAI API to deeply understand context, sentiment, and nuance in user feedback.
* **Automated Categorization**: Dynamically categorizes feedback and dynamically structures SQL tables to accommodate new data points (e.g., dynamically adding category columns).
* **Robust Database Integration**: Seamlessly connects to MySQL for persistent, queryable storage of analyzed feedback.
* **Secure Credentials Management**: Designed with security in mind, ensuring no hardcoded passwords or API keys are committed to version control.
* **DevContainer Support**: Comes with a ready-to-use `.devcontainer` configuration, providing a consistent, isolated development environment for all contributors.

---

## 🛠 Tech Stack

* **Language**: Python 3.x
* **AI/NLP**: OpenAI API
* **Database**: MySQL
* **Environment**: VS Code DevContainers, Virtual Environments (`venv`)

---

## 📂 Project Structure

```text
ai-feedback-analyzer/
├── .devcontainer/       # Configuration for VS Code Docker-based development
├── .gitignore           # Specifies intentionally untracked files to ignore (e.g., .env)
├── ai_pipeline.py       # Core logic for communicating with OpenAI and processing text
├── app.py               # Main application entry point and orchestration layer
├── requirements.txt     # Python dependencies (openai, mysql-connector, etc.)
└── README.md            # Project documentation
⚙️ Prerequisites
Before running the application locally, ensure you have the following installed:

Python 3.8+

MySQL Server (Running locally or hosted)

An active OpenAI API Key

🚀 Installation & Setup
1. Clone the repository

Bash
git clone [https://github.com/Saikiranpoluka/ai-feedback-analyzer.git](https://github.com/Saikiranpoluka/ai-feedback-analyzer.git)
cd ai-feedback-analyzer
2. Create a virtual environment

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install dependencies

Bash
pip install -r requirements.txt
🔐 Configuration
This project uses environment variables to keep sensitive information secure.

Create a .env file in the root directory (this file is git-ignored):

Bash
touch .env
Add your database credentials and API keys to the .env file:

Code snippet
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_secure_password
DB_NAME=feedback_db

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
Note: Ensure your MySQL database (feedback_db) is created before running the application.

💻 Usage
To run the application and start processing feedback, execute the main application script:

Bash
python app.py
Depending on your implementation in app.py, this will either start a local web server, trigger a batch processing job, or open an interactive CLI.*

🐳 Development Workflow (DevContainers)
For a frictionless development experience, this project includes a .devcontainer configuration.

Install Docker and the Dev Containers extension for VS Code.

Open the project folder in VS Code.

When prompted, click "Reopen in Container" (or use the command palette F1 -> Dev Containers: Reopen in Container).

VS Code will build the Docker image and set up a fully configured Python environment automatically.

🤝 Contributing
Contributions, issues, and feature requests are welcome!

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes securely, ensuring no sensitive data is included (git commit -m 'feat: Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📝 License
Distributed under the MIT License. See LICENSE for more information.
