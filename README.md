# PDF to DOCX Converter

A high-fidelity PDF to DOCX converter application that preserves the original layout, tables, images, and formatting. Built with a powerful Python backend and a modern, responsive frontend.

## Features

- **High-Fidelity Conversion**: Preserves complex layouts, tables, and images using advanced extraction logic.
- **Modern UI**: Clean, glassmorphism-inspired interface with drag-and-drop functionality.
- **Real-Time Progress**: Visual progress bar to track the conversion status.
- **FastAPI Backend**: High-performance REST API for handling file processing.
- **Secure Processing**: Files are processed locally and can be cleaned up automatically (logic extensible).

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, pdf2docx, PyMuPDF
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS
- **Design**: Glassmorphism UI, Inter Font

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1.  **Clone the repository** (or extract the project files):
    ```bash
    cd "d:/Govt docs/pdf_2_docx"
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment**:
    - Windows:
        ```bash
        .venv\Scripts\activate
        ```
    - Linux/Mac:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

## Usage

### 1. Start the Backend Server
Run the FastAPI server to handle conversions:
```bash
python backend/main.py
```
The server will start at `http://localhost:8000`.

### 2. Launch the Frontend
Open the `frontend/index.html` file in your web browser. You can do this by double-clicking the file or running:
```bash
start frontend/index.html
```

### 3. Convert Files
1.  Drag and drop a PDF file into the upload area.
2.  Wait for the conversion to complete (progress bar will fill up).
3.  Click **Download DOCX** to save your converted file.

## API Endpoints

- `POST /upload`: Upload a PDF file for conversion. Returns a `task_id`.
- `GET /status/{task_id}`: Check the status of a conversion task.
- `GET /download/{task_id}`: Download the converted DOCX file.

## Project Structure

```
pdf_2_docx/
├── backend/
│   ├── main.py          # FastAPI application entry point
│   ├── converter.py     # Core PDF to DOCX conversion logic
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── index.html       # Main user interface
│   ├── app.js           # Frontend logic and API integration
│   └── style.css        # (Optional) Additional styles
├── uploads/             # Temporary storage for uploaded PDFs
├── processed/           # Storage for converted DOCX files
└── README.md            # Project documentation
```

## Author

**Mithra Chada**
