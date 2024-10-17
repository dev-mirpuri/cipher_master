from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import os
from cryptography.fernet import Fernet
import base64

app = Flask(__name__, static_folder='static')
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the secret key from an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
FERNET_KEY = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32].ljust(32, b'\0'))
fernet = Fernet(FERNET_KEY)

# Serve static HTML file
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt(self, text):
        return ''.join([self.alphabet[(self.alphabet.index(c.lower()) + self.shift) % 26] if c.lower() in self.alphabet else c for c in text])

    def decrypt(self, text):
        return ''.join([self.alphabet[(self.alphabet.index(c.lower()) - self.shift) % 26] if c.lower() in self.alphabet else c for c in text])

class VigenereCipher:
    def __init__(self, key):
        self.key = key.lower()
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt(self, text):
        key_repeated = self._repeat_key(text)
        return ''.join([self.alphabet[(self.alphabet.index(c.lower()) + self.alphabet.index(k)) % 26] if c.lower() in self.alphabet else c
                        for c, k in zip(text, key_repeated)])

    def decrypt(self, text):
        key_repeated = self._repeat_key(text)
        return ''.join([self.alphabet[(self.alphabet.index(c.lower()) - self.alphabet.index(k)) % 26] if c.lower() in self.alphabet else c
                        for c, k in zip(text, key_repeated)])

    def _repeat_key(self, text):
        return (self.key * (len(text) // len(self.key) + 1))[:len(text)]

def process_text(action, data):
    cipher_type = data.get('cipher')
    text = data.get('text')
    key = data.get('key', '')

    logger.info(f"{action.capitalize()} request: {data}")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if cipher_type == 'caesar':
        try:
            shift = int(key)
            cipher = CaesarCipher(shift)
        except ValueError:
            return jsonify({"error": "Key for Caesar cipher must be a number"}), 400
    elif cipher_type == 'vigenere':
        if not key.isalpha():
            return jsonify({"error": "Key for Vigenère cipher must contain only letters"}), 400
        cipher = VigenereCipher(key)
    elif cipher_type == 'fernet':
        try:
            if action == 'encrypt':
                processed_text = fernet.encrypt(text.encode()).decode()
            else:
                processed_text = fernet.decrypt(text.encode()).decode()
            return jsonify({f"{action}ed_text": processed_text})
        except Exception as e:
            logger.error(f"Fernet {action} error: {str(e)}")
            return jsonify({"error": f"Error during Fernet {action}ion"}), 400
    else:
        return jsonify({"error": "Unsupported cipher type"}), 400

    if action == 'encrypt':
        processed_text = cipher.encrypt(text)
    else:
        processed_text = cipher.decrypt(text)

    return jsonify({f"{action}ed_text": processed_text})

@app.route('/encrypt', methods=['POST'])
def encrypt():
    return process_text('encrypt', request.get_json())

@app.route('/decrypt', methods=['POST'])
def decrypt():
    return process_text('decrypt', request.get_json())

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')