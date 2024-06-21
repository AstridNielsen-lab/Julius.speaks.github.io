function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var chatHistory = document.getElementById('chat-history');

    // Exibe a pergunta do usuário no histórico
    var userMessage = '<div class="message user-message"><p><strong>Você:</strong> ' + userInput + '</p></div>';
    chatHistory.innerHTML += userMessage;

    // Envia a pergunta para o servidor Flask
    fetch('/send_question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const assistantMessage = '<div class="message assistant-message"><p><strong>Assistente:</strong> ' + data.text + '</p></div>';
        chatHistory.innerHTML += assistantMessage;

        if (data.audio_base64) {
            playAudio(data.audio_base64);
        } else {
            console.error('Erro ao converter texto em áudio');
        }
    })
    .catch(error => {
        console.error('Erro ao enviar pergunta:', error);
    });

    // Limpa o campo de entrada do usuário
    document.getElementById('user-input').value = '';

    // Impede o envio do formulário
    return false;
}

// Função para reproduzir áudio a partir de base64
function playAudio(audioBase64) {
    var audio = new Audio();
    audio.src = 'data:audio/wav;base64,' + audioBase64;
    audio.play();
}

// Função para enviar mensagem ao pressionar Enter
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Impede a ação padrão de enviar o formulário
        sendMessage();
    }
});
