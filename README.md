# CUAD Legal Contract Analyzer using LLM

## Overview

The **CUAD Legal Contract Analyzer** is an AI-powered application that automatically analyzes legal contracts using Large Language Models (LLMs). It extracts important legal clauses, summarizes contracts, and stores the processed information for easy retrieval.

This project is built as part of the **Contract Understanding Atticus Dataset (CUAD)** take-home assignment.

---

# Objectives

* Load and preprocess legal contracts from the CUAD dataset.
* Extract text from PDF contracts.
* Normalize contract text.
* Use an LLM to identify important legal clauses.
* Generate concise contract summaries.
* Store extracted information in a database.
* Display results through a React-based user interface.

---

# Features

* PDF Contract Upload
* Automatic Text Extraction
* LLM-Based Clause Extraction
* Contract Summarization (100–150 words)
* SQLite Database Storage
* REST API using Flask
* Modern React Dashboard
* Search-ready contract embeddings

---

# Technology Stack

### Backend

* Python 3.11+
* Flask
* SQLAlchemy
* Flask-CORS
* PyMuPDF (fitz)
* Groq API
* Sentence Transformers

### Frontend

* React.js
* Axios
* Tailwind CSS
* Framer Motion
* Lucide React

### Database

* SQLite

---

# Project Structure

```
CUAD/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── pdf_proc.py
│   │   ├── llm_proc.py
│   │   ├── search.py
│   │   └── data/
│   │
│   ├── run.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── output/
│   └── contracts.json
│
└── README.md
```

---

# Workflow

```
PDF Contracts
      │
      ▼
Text Extraction
(PyMuPDF)
      │
      ▼
Text Cleaning
      │
      ▼
LLM Processing
      │
      ├──────────────► Contract Summary
      │
      ├──────────────► Termination Clause
      │
      ├──────────────► Confidentiality Clause
      │
      └──────────────► Liability Clause
      │
      ▼
Embedding Generation
      │
      ▼
SQLite Database
      │
      ▼
Flask REST API
      │
      ▼
React Dashboard
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/CUAD.git
cd CUAD
```

---

## Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=YOUR_API_KEY
DATABASE_URL=sqlite:///contracts.db
```

Run the backend:

```bash
python run.py
```

Backend runs at:

```
http://localhost:5000
```

---

## Frontend Setup

Navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React application:

```bash
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# API Endpoints

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| GET    | `/api/`                    | Health Check             |
| POST   | `/api/upload`              | Upload PDF               |
| POST   | `/api/process-cuad-subset` | Process Contracts        |
| GET    | `/api/contracts`           | List Processed Contracts |

---

# Output Format

Each processed contract contains:

```json
{
  "contract_id": 1,
  "summary": "Concise summary of the agreement...",
  "termination_clause": "...",
  "confidentiality_clause": "...",
  "liability_clause": "..."
}
```

The results can be exported as JSON or CSV.

---

# Approach

1. Upload legal contracts in PDF format.
2. Extract text using PyMuPDF.
3. Clean and normalize extracted text.
4. Send the text to the LLM.
5. Extract:

   * Termination Clause
   * Confidentiality Clause
   * Liability Clause
6. Generate a 100–150 word summary.
7. Generate embeddings for semantic search.
8. Store all processed information in SQLite.
9. Display results through the React dashboard.

---

# Future Improvements

* Multi-document semantic search
* RAG (Retrieval-Augmented Generation)
* Vector database integration (ChromaDB/FAISS)
* OCR support for scanned PDFs
* Clause comparison across contracts
* User authentication and role-based access
* Docker deployment
* Cloud deployment (Render + Vercel)

---

# Author

**Pemmadi Balu**

* B.Tech – Computer Science & Engineering (Artificial Intelligence & Data Science)
* Python | AI | Machine Learning | NLP | LLM | Flask | React

---

# License

This project is developed for educational and assessment purposes using the publicly available CUAD dataset.
