from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__)

# Tesseract'ın kurulu olduğu yolu belirtin
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    image = image.convert('L')  # Gri tonlama
    image = image.filter(ImageFilter.SHARPEN)  # Keskinleştirme
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Kontrastı artırma
    return image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya yüklenmedi'})
    file = request.files['file']
    lang = request.form.get('lang', 'eng')  # Varsayılan dil İngilizce
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'})
    if file:
        image = Image.open(file.stream)
        image = preprocess_image(image)
        custom_config = r'--oem 3 --psm 3 -c preserve_interword_spaces=1'
        text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
        return jsonify({'text': text})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
