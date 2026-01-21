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
    ```git clone https://github.com/yourusername/ai-pdf-processor.git```

    ```cd ai-pdf-processor```

2. Install dependencies
pip install -r requirements.txt

3. Set up Google GenAI API key


     Step 1: Go to [Google Cloud Console](https://console.cloud.google.com/).

     Step 2: Create a new project or select an existing project.

     Step 3: Navigate to **APIs & Services → Credentials**.

     Step 4: Click **Create Credentials → API Key**. Copy the generated key.

    Step 5: Enable the **Generative AI API** for your project:
   
   - Go to **APIs & Services → Library**
     
   - Search for **Generative AI API** and click **Enable**

4. Set the API key as an environment variable on your machine:


    ```export GOOGLE_API_KEY="your_api_key_here"```   # Linux/Mac

    ```set GOOGLE_API_KEY="your_api_key_here"```      # Windows

5. Run the app
```streamlit run app.py```

6. Open the browser, upload PDFs, and start asking questions

## Dependencies

- Python 3.9+
- Streamlit
- PyPDF
- Google GenAI Python Client

## Notes

- Make sure to upload only PDF files.
- Large PDFs may be truncated due to AI input limits.
- Q&A history is saved only for the current session.

