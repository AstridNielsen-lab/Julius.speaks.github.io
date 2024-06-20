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
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantMessage = '<div class="message assistant-message"><p><strong>Assistente:</strong> ';
        chatHistory.innerHTML += assistantMessage;

        function readStream() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    chatHistory.innerHTML += '</p></div>';
                    // Limpa o campo de entrada do usuário
                    document.getElementById('user-input').value = '';
                    // Rolagem automática para exibir a mensagem mais recente
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                    return;
                }
                const textChunk = decoder.decode(value, { stream: true });
                const formattedText = textChunk.replace(/<[^>]+>/g, '');  // Remove tags HTML
                chatHistory.lastChild.lastChild.innerHTML += formattedText;  // Adiciona o texto formatado ao histórico
                readStream();
            }).catch(error => {
                console.error('Erro ao ler o stream:', error);
            });
        }

        readStream();
    })
    .catch(error => {
        console.error('Erro ao enviar pergunta:', error);
    });

    // Impede o envio do formulário
    return false;
}

// Função para enviar mensagem ao pressionar Enter
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Impede a ação padrão de enviar o formulário
        sendMessage();
    }
});

// Função para converter texto em áudio usando o Azure Speech
function textToSpeech(text) {
    fetch('/text_to_speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.audio_base64) {
            playAudio(data.audio_base64);
        } else {
            console.error('Erro ao converter texto em áudio');
        }
    })
    .catch(error => {
        console.error('Erro na requisição para conversão de texto em áudio:', error);
    });
}

// Função para reproduzir áudio a partir de base64
function playAudio(audioBase64) {
    var audio = new Audio();
    audio.src = 'data:audio/wav;base64,' + audioBase64;
    audio.play();
}
