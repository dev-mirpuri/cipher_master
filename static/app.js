document.getElementById('encryptBtn').addEventListener('click', function() {
    processText('encrypt');
});

document.getElementById('decryptBtn').addEventListener('click', function() {
    processText('decrypt');
});

function processText(action) {
    const text = document.getElementById('inputText').value;
    const cipherType = document.getElementById('cipherType').value;
    const key = document.getElementById('keyInput').value;

    const data = {
        cipher: cipherType,
        text: text,
        key: key
    };

    fetch(`/${action}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (action === 'encrypt') {
            document.getElementById('outputText').textContent = `Encrypted Text: ${data.encrypted_text}`;
        } else {
            document.getElementById('outputText').textContent = `Decrypted Text: ${data.decrypted_text}`;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
