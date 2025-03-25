# AI Agent API

This repository contains a FastAPI-based application that provides an API for interacting with an AI agent. The agent can answer questions based on a knowledge base constructed from PDF documents and analyze user answers against guidelines with RAG documents as context. The application supports Qdrant vector stores for knowledge retrieval.

## Project Structure

The project has been restructured into a more modular organization for better maintainability and expandability:

```
root/
│
├── app/                    # Main application package
│   ├── api/                # API related modules
│   │   ├── endpoints/      # API endpoints
│   │   │   ├── health.py   # Health check endpoints
│   │   │   └── rag.py      # RAG functionality endpoints
│   │   └── middleware/     # API middleware
│   ├── core/               # Core functionality
│   │   ├── agent/          # Agent implementations
│   │   │   └── rag_agent.py # RAG agent implementation
│   │   └── config.py       # Configuration settings
│   ├── db/                 # Database interactions
│   │   └── qdrant.py       # Qdrant database connection
│   ├── models/             # Data models
│   │   └── schema.py       # Pydantic models for the API
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   │   └── document_loader.py # Document loading utilities
│   └── main.py             # FastAPI application initialization
│
├── data/                   # Data files
│   └── pdfs/               # PDF documents to be indexed
│
├── frontend/               # Frontend application
│   ├── css/                # CSS styles
│   ├── js/                 # JavaScript files
│   └── pages/              # HTML pages
│
├── scripts/                # Utility scripts
│   ├── load_documents.py   # Script for loading documents into Qdrant
│   └── run_api.py          # Script for running the FastAPI application
│
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── run.py                  # Convenience runner script
└── README.md               # Project documentation
```

## Features

- **Question Answering**: Ask questions to the AI agent and receive responses based on indexed knowledge.
- **Answer Analysis**: Analyze user answers against guidelines and provide detailed feedback.
- **Health Check**: Simple endpoint to verify the API is running.
- **CORS Support**: Configured to allow cross-origin requests.

## Setup

### Prerequisites

- Python 3.8+
- Qdrant (for vector storage)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   OPENAI_API_KEY=<your-openai-api-key>
   QDRANT_URL=<your-qdrant-url>
   QDRANT_API_KEY=<your-qdrant-api-key>
   ```

### Loading Documents

Before running the API, you need to load documents into the Qdrant vector database:

```bash
python scripts/load_documents.py --dir ./data/pdfs --module module1
```

You can customize the directory containing PDF files and the module identifier for the collection name.

### Running the Application Locally

There are two ways to run the application:

1. **Using the run.py script**:
   ```bash
   python run.py
   ```

2. **Using the scripts/run_api.py script**:
   ```bash
   python scripts/run_api.py --reload
   ```

The `--reload` flag enables auto-reload for development.

### Access the API Documentation

Open your browser and go to `http://localhost:8000/docs` to view the interactive API documentation.

## API Endpoints

- **`/ask_bot`**: Sends a question to the LangGraph agent using Qdrant vector store with streaming response.
- **`/analyze_answer`**: Analyzes the user's answer against guidelines using RAG-generated context.
- **`/`**: Health check endpoint to verify the API is running.

## License

This project is licensed under the MIT License.

## Contact

For support, please contact [support@example.com](mailto:support@example.com).
