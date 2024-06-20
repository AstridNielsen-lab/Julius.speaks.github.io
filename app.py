import asyncio
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import openai
import azure.cognitiveservices.speech as speechsdk
import base64

app = Flask(__name__)

# Configurações da OpenAI
openai.api_key = "sk-proj-YL6DGd50XwDxbv0C9CByT3BlbkFJrJG5mz2ZkD8PHbZyXJ9x"

# Configurações do Azure Speech
azure_api_key = "d00ed40fcc144be0a167721cf5867bee"
azure_region = "westeurope"

# Lista para armazenar respostas
responses = []

# Inicialização do serviço de fala da Azure
speech_config = speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)
speech_config.speech_synthesis_voice_name = 'sr-RS-NicholasNeural'  # Exemplo de voz para o idioma sérvio

# Função para enviar a pergunta ao assistente da OpenAI
@app.route('/send_question', methods=['POST'])
def send_question():
    try:
        user_question = request.json['question']

        @stream_with_context
        def generate():
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente útil."},
                    {"role": "user", "content": user_question}
                ],
                stream=True
            )
            for chunk in response:
                if 'choices' in chunk:
                    text_chunk = chunk['choices'][0]['delta'].get('content', '')
                    yield text_chunk

        return Response(generate(), content_type='text/plain')

    except Exception as e:
        print(f"Erro ao enviar pergunta para o assistente da OpenAI: {e}")
        return jsonify({'response': 'Erro ao enviar pergunta para o assistente da OpenAI'}), 500

# Função para converter texto em áudio usando Azure Speech
def text_to_speech(text):
    try:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_stream = result.audio_data
            audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
            return audio_base64
        else:
            print(f"Erro ao sintetizar áudio: {result.reason}")
            return None
    except Exception as e:
        print(f"Erro ao converter texto em áudio com Azure Speech: {e}")
        return None

# Rota para converter texto em áudio
@app.route('/text_to_speech', methods=['POST'])
def convert_text_to_speech():
    try:
        data = request.json
        text = data['text']
        audio_base64 = text_to_speech(text)
        if audio_base64:
            return jsonify({'audio_base64': audio_base64}), 200
        else:
            return jsonify({'error': 'Erro ao converter texto em áudio'}), 500
    except Exception as e:
        print(f"Erro na conversão de texto para áudio: {e}")
        return jsonify({'error': 'Erro na conversão de texto para áudio'}), 500

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html', responses=responses)

if __name__ == '__main__':
    app.run(debug=True)
