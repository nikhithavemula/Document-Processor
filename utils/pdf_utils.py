from pypdf import PdfReader

# Define a function that extracts readable text from a given PDF file.
def extract_text_from_pdf(file_path: str) -> str:
    # Document the purpose and behavior of this function.
    """
    Safely extract text from a PDF.
    Skips pages with broken fonts instead of crashing.
    """

    # Create a PDF reader object using the provided file path.
    reader = PdfReader(file_path)

    # Initialize a list to store extracted text from each valid page.
    extracted_pages = []

    # Loop through each page in the PDF with its index.
    for i, page in enumerate(reader.pages):
        try:
            # Attempt to extract text from the current page.
            text = page.extract_text()

            # Add the extracted text only if the page contains readable content.
            if text:
                extracted_pages.append(text)

        except Exception:
            # Ignore pages that cause errors due to font or layout issues.
            continue

    # Combine all extracted page text into a single string separated by new lines.
    return "\n".join(extracted_pages)