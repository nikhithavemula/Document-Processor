# Set page title and layout
st.set_page_config(page_title="AI PDF Question Answering", layout="centered")  
# Display the main title of the app
st.title("AI PDF Question Answering")  

# Initialize the Google AI client
client = genai.Client()  

# -------------------------------------------------
# Helpers
# -------------------------------------------------
# Extract JSON from AI response text
def extract_json(text: str) -> str:  
    # Remove ```json code blocks
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)  
    # Remove any leftover ```
    text = re.sub(r"```", "", text)  
    # Find JSON object in text
    match = re.search(r"\{.*\}", text, re.DOTALL)  
    # If no JSON found, raise an error
    if not match:  
        raise ValueError("No JSON found")  
    # Return the extracted JSON string
    return match.group(0)  


# Split text into chunks with overlap
def chunk_text(text: str, chunk_size=800, overlap=100):  
    # Initialize list to hold chunks
    chunks = []  
    # Starting index
    start = 0  
    # Continue until all text is chunked
    while start < len(text):  
        # Calculate chunk end
        end = start + chunk_size  
        # Add chunk to list
        chunks.append(text[start:end])  
        # Move start index with overlap
        start = end - overlap  
    # Return all chunks
    return chunks  

# -------------------------------------------------
# Session state
# -------------------------------------------------
# Store text chunks in session state
st.session_state.setdefault("chunks", [])  
# Track last uploaded files
st.session_state.setdefault("last_files", None)  
# Track Q&A history
st.session_state.setdefault("qa_history", [])  

# -------------------------------------------------
# File uploader
# -------------------------------------------------
# Display PDF file uploader, accepting only the pdf files and allowing multiple files to upload
uploaded_files = st.file_uploader(  
    "Upload PDF files",
    type=["pdf"],  
    accept_multiple_files=True  
)

# -------------------------------------------------
# Process PDFs immediately
# -------------------------------------------------
# If files are uploaded
if uploaded_files:  
    # Get tuple of uploaded file names
    current_files = tuple(f.name for f in uploaded_files)  

    # Only process if new files
    if current_files != st.session_state.last_files:  
        # Update last uploaded files
        st.session_state.last_files = current_files  
        # Reset stored text chunks
        st.session_state.chunks = []  
        # Reset Q&A history
        st.session_state.qa_history = []  

        # Show spinner while processing
        with st.spinner("Processing documents..."):  
            # Loop through each uploaded file
            for f in uploaded_files:  
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:  
                    # Write PDF content to temp file
                    tmp.write(f.read())  
                    # Save temp file path
                    path = tmp.name  

                # Extract text from PDF
                text = extract_text_from_pdf(path)  
                # Delete temp file after reading
                os.remove(path)  

                # If text exists
                if text:  
                    # Split text into chunks and store
                    st.session_state.chunks.extend(chunk_text(text))  

        # Show number of chunks loaded
        st.success(f"Loaded {len(st.session_state.chunks)} text chunks.")  

# -------------------------------------------------
# Stable Question UI (NO flicker)
# -------------------------------------------------
# Placeholder for Q&A form
qa_container = st.empty()  

# Render Q&A form container
with qa_container.container():  
    # Form that clears on submit
    with st.form("qa_form", clear_on_submit=True):  
        # Split into two columns
        col1, col2 = st.columns([8, 1])  

        # Left column for input, input label, placeholder text, disable if no chunks loaded
        with col1:  
            question = st.text_input(
                "Ask a question about the documents", 
                placeholder="Type your question and press Enter", 
                disabled=not bool(st.session_state.chunks)  
            )

        # Right column for submit button
        with col2:  
            # Spacer for alignment
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)  
            # Submit button
            send = st.form_submit_button("Send")  

        # Track if the form was submitted
        submitted = send  

# -------------------------------------------------
# Question answering
# -------------------------------------------------
# If the form is submitted
if submitted:  
    # Check for empty question
    if not question.strip():  
        # Show warning
        st.warning("Please enter a question.")  
    else:
        # Combine all text chunks into context
        context = "\n\n".join(st.session_state.chunks)  

        # Build prompt for AI
        prompt = f"""  
You are a document analysis assistant.

Rules:
- Use ONLY the provided document content
- Answer strictly in JSON
- Do NOT include markdown or explanations
- If the answer is not found, say so clearly

Return JSON in this format:
{{
  "answer": "<answer text>",
  "documents_used": []
}}

Documents:
{context}

Question:
{question}
"""

        # Try to generate answer using AI
        try:
            # Show spinner while AI generates answer
            with st.spinner("Analyzing documents..."):  
                # Call AI model
                response = client.models.generate_content(  
                    model="models/gemini-flash-latest",
                    contents=prompt
                )

            # Parse AI response JSON
            parsed = json.loads(extract_json(response.text))  
            # Extract answer text
            answer = parsed.get("answer", "").strip()  

            # Save Q&A to history
            st.session_state.qa_history.append(  
                {"question": question, "answer": answer}
            )

        # Handle errors
        except Exception as e:  
            # Convert exception to string
            msg = str(e)  
            # Check for rate limit errors
            if "RESOURCE_EXHAUSTED" in msg or "429" in msg:  
                # Show rate limit message
                st.error("⚠️ Rate limit hit. Please wait a moment and try again.")  
            else:
                # Show generic error message
                st.error("An unexpected error occurred.")  
                # Display full error details
                st.text(msg)  

# -------------------------------------------------
# Render Q&A history
# -------------------------------------------------
# If Q&A history exists
if st.session_state.qa_history:  
    # Display heading
    st.subheader("Answer")  
    # Loop through history in reverse
    for item in reversed(st.session_state.qa_history):  
        # Display question
        st.markdown(f"**Q:** {item['question']}")  
        # Display answer
        st.write(item["answer"])  
