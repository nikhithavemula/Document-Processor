# AI PDF Question Answering

A simple AI-powered app that lets you upload PDF files and ask natural language questions about them. The app extracts text from PDFs, processes it, and uses Google’s Generative AI models (ADK) to give JSON-formatted answers along with the source documents.

## What it does

- Upload 2–3 PDF files
- Extract and process text safely from PDFs
- Ask questions about the documents in natural language
- Receive JSON answers with document references
- Keep Q&A history in the session

## Setup and Run

1. Clone the repo
git clone https://github.com/yourusername/ai-pdf-processor.git
cd ai-pdf-processor

2. Install dependencies
pip install -r requirements.txt

3. Set up Google GenAI API key
export GOOGLE_API_KEY="your_api_key_here"   # Linux/Mac
set GOOGLE_API_KEY="your_api_key_here"      # Windows

4. Run the app
```streamlit run app.py```

5. Open the browser, upload PDFs, and start asking questions

## Dependencies

- Python 3.9+
- Streamlit
- PyPDF
- Google GenAI Python Client
