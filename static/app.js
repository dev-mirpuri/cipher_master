document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const cipherType = document.getElementById('cipherType');
    const keyInput = document.getElementById('keyInput');
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    const outputText = document.getElementById('outputText');
    const copyBtn = document.getElementById('copyBtn');

    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.textContent = message;
        notification.className = `fixed top-4 right-4 p-4 rounded text-white ${type === 'error' ? 'bg-red-500' : 'bg-green-500'}`;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    function processText(action) {
        const text = inputText.value.trim();
        const cipher = cipherType.value;
        const key = keyInput.value.trim();

        if (!text) {
            showNotification('Please enter some text to process.', 'error');
            return;
        }

        if (cipher !== 'fernet' && !key) {
            showNotification('Please enter a key.', 'error');
            return;
        }

        const data = { cipher, text, key };

        fetch(`/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification(data.error, 'error');
            } else {
                outputText.textContent = data[`${action}ed_text`];
                showNotification(`Text ${action}ed successfully!`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        });
    }

    encryptBtn.addEventListener('click', () => processText('encrypt'));
    decryptBtn.addEventListener('click', () => processText('decrypt'));

    copyBtn.addEventListener('click', () => {
        const textToCopy = outputText.textContent;
        if (textToCopy) {
            navigator.clipboard.writeText(textToCopy)
                .then(() => showNotification('Copied to clipboard!'))
                .catch(err => {
                    console.error('Error copying text: ', err);
                    showNotification('Failed to copy text.', 'error');
                });
        } else {
            showNotification('No text to copy.', 'error');
        }
    });

    cipherType.addEventListener('change', () => {
        const isFernet = cipherType.value === 'fernet';
        keyInput.placeholder = isFernet ? 'No key required for Fernet' : 'Enter key (or shift for Caesar)';
        keyInput.disabled = isFernet;
    });
});