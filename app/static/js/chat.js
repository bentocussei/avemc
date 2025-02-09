document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');

    // Função para adicionar mensagem ao chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'} mb-3`;
        messageDiv.innerHTML = `
            <div class="message-content">
                <p class="mb-0">${message}</p>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função para mostrar indicador de digitação
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message mb-3';
        typingDiv.innerHTML = `
            <div class="message-content typing">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        typingDiv.id = 'typing-indicator';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Função para remover indicador de digitação
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Manipular envio do formulário
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (message) {
            // Adiciona mensagem do usuário
            addMessage(message, true);
            userInput.value = '';

            // Mostra indicador de digitação
            showTypingIndicator();

            try {
                // Aqui você fará a chamada para sua API
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                // Remove indicador de digitação e adiciona resposta do bot
                setTimeout(() => {
                    removeTypingIndicator();
                    addMessage(data.response);
                }, 1000); // Simula tempo de resposta

            } catch (error) {
                console.error('Erro:', error);
                removeTypingIndicator();
                addMessage('Desculpe, ocorreu um erro ao processar sua mensagem.');
            }
        }
    });

    // Manipular cliques nas sugestões
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            userInput.value = this.textContent;
            userInput.focus();
        });
    });
}); 