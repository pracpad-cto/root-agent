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
- **User Authentication**: JWT-based authentication with role-based access control.
- **User Management**: Create and manage users with different roles.
- **OCR Capabilities**: Process scanned image-based PDFs using optical character recognition.
- **Health Check**: Simple endpoint to verify the API is running.
- **CORS Support**: Configured to allow cross-origin requests.

## Authentication System

The application features a comprehensive JWT-based authentication system with role-based access control:

### User Roles

- **Regular User**: Basic access to the application
- **Admin**: Access to user management and administrative functions
- **Super Admin**: Full access to all features including the ability to create other admin users

### Authentication Endpoints

- **POST /login**: Authenticate a user and receive a JWT token
- **POST /register**: Register a new user account (public endpoint)
- **GET /me**: Get current user information
- **GET /admin**: Admin-only test endpoint
- **GET /superadmin**: Superadmin-only test endpoint

### User Management Endpoints

- **GET /users**: Get all users (admin access only)
- **POST /users**: Create a new user (with role-based restrictions)
- **GET /users/{user_id}**: Get a specific user (users can view their own profile, admins can view all)

### API Access Requirements

All endpoints, except the following public endpoints, require authentication:
- **POST /login**: User authentication
- **POST /register**: User registration
- **GET /**: Health check endpoint

## Setup

### Prerequisites

- Python 3.8+
- Qdrant (for vector storage)
- Tesseract OCR (for processing scanned documents)
- Poppler (for PDF to image conversion)

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

4. **Install Tesseract OCR and Poppler**:
   
   For Windows:
   ```bash
   # Install Tesseract OCR
   # Download installer from https://github.com/UB-Mannheim/tesseract/wiki
   
   # Install Poppler
   # Download from https://github.com/oschwartz10612/poppler-windows/releases/
   ```
   
   For macOS:
   ```bash
   brew install tesseract
   brew install poppler
   ```
   
   For Ubuntu/Debian:
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   sudo apt-get install poppler-utils
   ```

5. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```plaintext
   OPENAI_API_KEY=<your-openai-api-key>
   QDRANT_URL=<your-qdrant-url>
   QDRANT_API_KEY=<your-qdrant-api-key>
   DATABASE_URL=<your-database-url>
   
   # OCR settings
   POPPLER_PATH=<path-to-poppler-bin-directory>  # e.g., C:\path\to\poppler\bin
   
   # JWT Authentication settings
   SECRET_KEY=<your-secret-key>
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```

   For production, generate a secure random secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Loading Documents

Before running the API, you need to load documents into the Qdrant vector database:

```bash
python scripts/load_documents.py --dir ./data/pdfs --module module1
```

You can customize the directory containing PDF files and the module identifier for the collection name.

#### OCR Processing Options

For documents that are scanned images, the loader will automatically use OCR:

```bash
# With OCR enabled (default)
python scripts/load_documents.py --dir ./data/pdfs --module module1

# Disable OCR processing
python scripts/load_documents.py --dir ./data/pdfs --module module1 --no-ocr
```

The document loader first attempts to extract text directly from PDFs. If insufficient text is found, it automatically falls back to OCR processing.

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

### Setting Up Authentication

After setting up your environment variables, create a superadmin user:

```bash
python scripts/create_superadmin.py --email admin@example.com --password YourPassword
```

You can customize the email, password, first name, and last name using command-line arguments.

### Securing Endpoints

To access secured endpoints, first obtain a JWT token:

1. POST to `/login` with your credentials
2. Include the returned token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <your-token>
   ```

Alternatively, new users can register by sending a POST request to `/register` with the required user information.
