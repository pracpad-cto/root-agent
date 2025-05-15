# How to Upload PDF Documents to Qdrant Vector Database

This guide explains how to use the `load_documents.py` script to upload PDF files to the Qdrant vector database for use with the PracPad application.

## Prerequisites

1. Ensure you have installed all required dependencies listed in `requirements.txt`
2. Make sure you have configured your `.env` file with the required API keys:
   - `OPENAI_API_KEY` - Required for generating embeddings

## Optional Requirements for OCR Support

If you plan to upload scanned PDFs (image-based documents), you'll need:

1. Pytesseract - Already in requirements.txt
2. Poppler - PDF to image conversion tool:
   - Windows: Download from [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Mac: `brew install poppler`
   - Linux: `apt-get install poppler-utils`

## Basic Usage

1. Place your PDF files in the `data/pdfs` directory
2. Run the script with default settings:

```bash
python scripts/load_documents.py
```

This will:
- Process all PDFs in the `data/pdfs` directory
- Use OCR if standard text extraction fails
- Store embeddings in a collection named after the default module ("module1")

## Advanced Usage

### Command-line Arguments

```bash
python scripts/load_documents.py [options]
```

Available options:

| Option | Description | Default |
|--------|-------------|---------|
| `--dir` | Directory containing PDF files | `./data/pdfs` |
| `--module` | Module identifier for collection name | `module1` |
| `--recreate` | Recreate collection if it exists | `False` |
| `--no-ocr` | Disable OCR processing for scanned docs | `False` |
| `--poppler-path` | Path to Poppler binaries | Value from env var `POPPLER_PATH` |

### Examples

#### Upload PDFs to a specific module collection:

```bash
python scripts/load_documents.py --module legal_docs
```

#### Upload PDFs from a custom directory:

```bash
python scripts/load_documents.py --dir ./my_custom_pdfs
```

#### Recreate an existing collection:

```bash
python scripts/load_documents.py --module module1 --recreate
```

#### Disable OCR (for faster processing if all documents are text-based):

```bash
python scripts/load_documents.py --no-ocr
```

#### Specify Poppler path for OCR:

```bash
python scripts/load_documents.py --poppler-path C:\path\to\poppler\bin
```

## Understanding the Process

When you run the script:

1. The system iterates through all PDFs in the specified directory
2. For each PDF:
   - First attempts standard text extraction with PyPDF
   - If that yields insufficient text (likely a scanned document), it uses OCR if enabled
3. Text is split into manageable chunks (~500 characters with 50 character overlap)
4. OpenAI's embedding API creates vector representations of each chunk
5. Chunks and their vectors are stored in Qdrant with appropriate metadata

## Troubleshooting

### OCR Not Working

If OCR isn't working correctly:
1. Ensure Poppler is installed and the path is correctly set
2. Verify you have pytesseract installed
3. Try running with explicit poppler path: `--poppler-path /path/to/poppler/bin`

### API Rate Limits

The script processes documents in batches to avoid OpenAI API rate limits. If you're processing a large number of documents and encounter rate limit errors:
1. Wait a few minutes and run again with the same parameters

### Checking Results

After uploading, the documents will be available in the Qdrant collection with the name based on the module identifier:
- Default: `pracpad_module1_docs`
- Custom module: `pracpad_[module]_docs` 