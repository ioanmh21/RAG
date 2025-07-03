const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.getElementById('chat-messages');

// Adresa URL a backend-ului tău FastAPI
// Asigură-te că aceasta corespunde cu host-ul și portul pe care rulează FastAPI.
const BACKEND_URL = 'http://127.0.0.1:8000'; 

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Funcție pentru a trimite mesajul către backend
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    addMessage(question, 'user'); // Afișează mesajul utilizatorului
    userInput.value = '';
    sendButton.disabled = true;

    const loadingIndicator = document.createElement('div');
    loadingIndicator.classList.add('loading-indicator');
    loadingIndicator.textContent = 'Asistentul gândește...';
    chatMessages.appendChild(loadingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${BACKEND_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: question }), // Trimite întrebarea ca obiect JSON
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        addMessage(data.answer, 'ai'); // Afișează răspunsul AI

    } catch (error) {
        console.error('Eroare la trimiterea mesajului:', error);
        addMessage(`Ne pare rău, a apărut o eroare: ${error.message}. Vă rugăm să încercați din nou.`, 'ai');
    } finally {
        sendButton.disabled = false;
        if (loadingIndicator.parentNode) {
            loadingIndicator.parentNode.removeChild(loadingIndicator);
        }
        userInput.focus();
    }
}

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

window.onload = () => {
    userInput.focus();
};