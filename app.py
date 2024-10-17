from flask import Flask, request, jsonify, send_from_directory
import logging

app = Flask(__name__, static_folder='static')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Serve static HTML file
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Encryption and decryption routes
class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt(self, text):
        return ''.join([self.alphabet[(self.alphabet.index(c) + self.shift) % 26] if c in self.alphabet else c for c in text.lower()])

    def decrypt(self, text):
        return ''.join([self.alphabet[(self.alphabet.index(c) - self.shift) % 26] if c in self.alphabet else c for c in text.lower()])

class VigenereCipher:
    def __init__(self, key):
        self.key = key.lower()
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def encrypt(self, text):
        key_repeated = self._repeat_key(text)
        return ''.join([self.alphabet[(self.alphabet.index(c) + self.alphabet.index(k)) % 26] if c in self.alphabet else c
                        for c, k in zip(text.lower(), key_repeated)])

    def decrypt(self, text):
        key_repeated = self._repeat_key(text)
        return ''.join([self.alphabet[(self.alphabet.index(c) - self.alphabet.index(k)) % 26] if c in self.alphabet else c
                        for c, k in zip(text.lower(), key_repeated)])

    def _repeat_key(self, text):
        return (self.key * (len(text) // len(self.key) + 1))[:len(text)]


# Route for encrypting text
@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    cipher_type = data.get('cipher')
    text = data.get('text')
    key = data.get('key', None)

    logging.info(f"Encryption request: {data}")

    if cipher_type == 'caesar':
        try:
            shift = int(key)
        except ValueError:
            return jsonify({"error": "Key for Caesar cipher must be a number"}), 400
        cipher = CaesarCipher(shift)
        encrypted_text = cipher.encrypt(text)
    elif cipher_type == 'vigenere':
        if not key.isalpha():
            return jsonify({"error": "Key for Vigenère cipher must contain only letters"}), 400
        cipher = VigenereCipher(key)
        encrypted_text = cipher.encrypt(text)
    else:
        return jsonify({"error": "Unsupported cipher type"}), 400

    return jsonify({"encrypted_text": encrypted_text})


# Route for decrypting text
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    cipher_type = data.get('cipher')
    text = data.get('text')
    key = data.get('key', None)

    logging.info(f"Decryption request: {data}")

    if cipher_type == 'caesar':
        try:
            shift = int(key)
        except ValueError:
            return jsonify({"error": "Key for Caesar cipher must be a number"}), 400
        cipher = CaesarCipher(shift)
        decrypted_text = cipher.decrypt(text)
    elif cipher_type == 'vigenere':
        if not key.isalpha():
            return jsonify({"error": "Key for Vigenère cipher must contain only letters"}), 400
        cipher = VigenereCipher(key)
        decrypted_text = cipher.decrypt(text)
    else:
        return jsonify({"error": "Unsupported cipher type"}), 400

    return jsonify({"decrypted_text": decrypted_text})


if __name__ == '__main__':
    app.run(debug=True)
