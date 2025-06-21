# Word to PDF Converter Web App

This is a Flask-based web application that allows users to upload Word files (.docx) and convert them to PDF and other formats (txt, html).

## Features
- Upload .docx files
- Convert to PDF, TXT, or HTML
- Download the converted file

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   flask run
   ```

## Notes
- Ensure LibreOffice is installed for PDF conversion.
- For other formats, pypandoc or python-docx is used.
