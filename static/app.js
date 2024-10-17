document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const cipherType = document.getElementById('cipherType');
    const keyInput = document.getElementById('keyInput');
    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    const outputText = document.getElementById('outputText');
    const copyBtn = document.getElementById('copyBtn');
    const notification = document.getElementById('notification');

    function showNotification(message) {
        notification.textContent = message;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    function validateInput() {
        if (!inputText.value.trim()) {
            showNotification('Please enter some text to encrypt/decrypt.');
            return false;
        }
        if (!keyInput.value.trim()) {
            showNotification('Please enter a key or shift value.');
            return false;
        }
        if (cipherType.value === 'caesar' && isNaN(keyInput.value)) {
            showNotification('Please enter a numeric shift value for Caesar cipher.');
            return false;
        }
        return true;
    }

    async function processText(action) {
        if (!validateInput()) return;

        const data = {
            cipher: cipherType.value,
            text: inputText.value,
            key: keyInput.value
        };

        try {
            const response = await fetch(`/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            outputText.textContent = action === 'encrypt' ? result.encrypted_text : result.decrypted_text;
            showNotification(`Text ${action}ed successfully!`);
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.');
        }
    }

    encryptBtn.addEventListener('click', () => processText('encrypt'));
    decryptBtn.addEventListener('click', () => processText('decrypt'));

    copyBtn.addEventListener('click', () => {
        if (!outputText.textContent) {
            showNotification('No text to copy!');
            return;
        }
        navigator.clipboard.writeText(outputText.textContent)
            .then(() => showNotification('Copied to clipboard!'))
            .catch(err => {
                console.error('Error copying text: ', err);
                showNotification('Failed to copy text. Please try again.');
            });
    });

    // Add animation to the input text area
    inputText.addEventListener('focus', () => {
        inputText.style.boxShadow = '0 0 10px rgba(74, 144, 226, 0.5)';
    });

    inputText.addEventListener('blur', () => {
        inputText.style.boxShadow = 'none';
    });

    // Dynamic key input label
    cipherType.addEventListener('change', () => {
        const label = document.querySelector('label[for="keyInput"]');
        label.textContent = cipherType.value === 'caesar' ? 'Shift Value:' : 'Encryption Key:';
    });
});