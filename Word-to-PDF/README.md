# Word ↔ PDF Converter Web App

This is a Flask-based web application that allows users to upload Word files (.docx) or PDF files and convert between Word and PDF formats securely in the browser.

## Features
- Upload .docx or .pdf files
- Convert Word to PDF (using LibreOffice)
- Convert PDF to Word (.docx) (using pdf2docx)
- Download the converted file (manual download button)
- No files are permanently saved on the server
- Minimal, secure, and easy to use

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
3. Ensure LibreOffice is installed for Word to PDF conversion:
   ```bash
   sudo apt-get update && sudo apt-get install -y libreoffice
   ```
4. Run the app:
   ```bash
   flask run
   ```

