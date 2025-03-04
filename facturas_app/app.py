import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from models import FacturaProcessor

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    texto_extraido = None
    factura_url = None

    if request.method == 'POST':
        if 'factura' not in request.files:
            return redirect(request.url)
        
        file = request.files['factura']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extraer texto de la imagen
            texto_extraido = FacturaProcessor.extraer_texto(filepath)

            factura_url = url_for('static', filename=f'uploads/{filename}')

    return render_template('index.html', texto=texto_extraido, factura_url=factura_url)



if __name__ == "__main__":
    app.run(debug=True)
