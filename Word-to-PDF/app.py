from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
import os
import uuid
import subprocess
from io import BytesIO
from pdf2docx import Converter

ALLOWED_EXTENSIONS = {'docx', 'pdf'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = file.filename
        ext = filename.rsplit('.', 1)[1].lower()
        file_id = str(uuid.uuid4())
        temp_upload = BytesIO(file.read())
        temp_upload.seek(0)
        output_format = request.form.get('format')
        try:
            if ext == 'docx' and output_format == 'pdf':
                temp_input_path = f'/tmp/{file_id}_{filename}'
                with open(temp_input_path, 'wb') as f:
                    f.write(temp_upload.read())
                temp_upload.seek(0)
                libreoffice_cmd = [
                    'libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', '--outdir', '/tmp', temp_input_path
                ]
                result = subprocess.run(libreoffice_cmd, capture_output=True)
                if result.returncode != 0:
                    os.remove(temp_input_path)
                    raise Exception(f'LibreOffice error: {result.stderr.decode()}')
                base_name = os.path.splitext(os.path.basename(temp_input_path))[0]
                temp_output_path = f'/tmp/{base_name}.pdf'
                os.remove(temp_input_path)
                session['pdf_path'] = temp_output_path
                session['pdf_name'] = base_name + '.pdf'
                return render_template('index.html', show_download=True, show_docx_download=False)
            elif ext == 'pdf' and output_format == 'docx':
                temp_input_path = f'/tmp/{file_id}_{filename}'
                with open(temp_input_path, 'wb') as f:
                    f.write(temp_upload.read())
                temp_upload.seek(0)
                base_name = os.path.splitext(os.path.basename(temp_input_path))[0]
                temp_output_path = f'/tmp/{base_name}.docx'
                try:
                    cv = Converter(temp_input_path)
                    cv.convert(temp_output_path, start=0, end=None)
                    cv.close()
                except Exception as e:
                    os.remove(temp_input_path)
                    raise Exception(f'pdf2docx error: {e}')
                os.remove(temp_input_path)
                session['docx_path'] = temp_output_path
                session['docx_name'] = base_name + '.docx'
                return render_template('index.html', show_download=False, show_docx_download=True)
            else:
                flash('Invalid conversion selection or file type.')
                return redirect(request.url)
        except Exception as e:
            flash(f'Conversion failed: {e}')
            return redirect(request.url)
    return render_template('index.html', show_download=False, show_docx_download=False)

@app.route('/download', methods=['GET'])
def download_pdf():
    pdf_path = session.get('pdf_path')
    pdf_name = session.get('pdf_name', 'converted.pdf')
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        os.remove(pdf_path)
        session.pop('pdf_path', None)
        session.pop('pdf_name', None)
        return send_file(BytesIO(pdf_bytes), as_attachment=True, download_name=pdf_name, mimetype='application/pdf')
    flash('No converted file available. Please convert a file first.')
    return redirect(url_for('index'))

@app.route('/download-docx', methods=['GET'])
def download_docx():
    docx_path = session.get('docx_path')
    docx_name = session.get('docx_name', 'converted.docx')
    if docx_path and os.path.exists(docx_path):
        with open(docx_path, 'rb') as f:
            docx_bytes = f.read()
        os.remove(docx_path)
        session.pop('docx_path', None)
        session.pop('docx_name', None)
        return send_file(BytesIO(docx_bytes), as_attachment=True, download_name=docx_name, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    flash('No converted file available. Please convert a file first.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
