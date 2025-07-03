const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.getElementById('chat-messages');

// Adresa URL a backend-ului tău FastAPI
// Asigură-te că aceasta corespunde cu host-ul și portul pe care rulează FastAPI.
// De obicei, pentru dezvoltare locală, este http://127.0.0.1:8000
const BACKEND_URL = 'http://127.0.0.1:8000'; 

// Funcție pentru a adăuga un mesaj în fereastra de chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    // Scrollează automat la ultimul mesaj
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Funcție pentru a trimite mesajul către backend
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return; // Nu trimite mesaje goale

    addMessage(question, 'user'); // Afișează mesajul utilizatorului
    userInput.value = ''; // Golește câmpul de intrare
    sendButton.disabled = true; // Dezactivează butonul în timpul procesării

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
        sendButton.disabled = false; // Reactivează butonul
        if (loadingIndicator.parentNode) {
            loadingIndicator.parentNode.removeChild(loadingIndicator); // Elimină indicatorul de încărcare
        }
        userInput.focus(); // Pune focus înapoi pe câmpul de intrare
    }
}

// Adaugă evenimente pentru buton și Enter
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Pune focus pe câmpul de intrare la încărcarea paginii
window.onload = () => {
    userInput.focus();
};