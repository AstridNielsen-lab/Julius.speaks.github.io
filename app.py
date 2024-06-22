import asyncio
from flask import Flask, render_template, request, jsonify
import openai
import azure.cognitiveservices.speech as speechsdk
import base64
import io

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
speech_config.speech_synthesis_voice_name = 'pt-BR-AntonioNeural'  # Voz em português do Brasil

# Função para enviar a pergunta ao assistente da OpenAI
@app.route('/send_question', methods=['POST'])
def send_question():
    try:
        user_question = request.json['question']

        def generate_response():
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente útil."},
                    {"role": "user", "content": user_question}
                ],
                stream=False  # Desativar o streaming para capturar a resposta completa
            )
            complete_text = response['choices'][0]['message']['content']
            return complete_text

        complete_text = generate_response()
        audio_base64 = text_to_speech(complete_text)

        return jsonify({
            'text': complete_text,
            'audio_base64': audio_base64
        })

    except Exception as e:
        print(f"Erro ao enviar pergunta para o assistente da OpenAI: {e}")
        return jsonify({'response': 'Erro ao enviar pergunta para o assistente da OpenAI'}), 500

# Função para converter texto em áudio usando Azure Speech
def text_to_speech(text):
    try:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)  # Ativa o alto-falante padrão
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_stream = io.BytesIO()
            audio_data_stream = speechsdk.AudioDataStream(result)
            audio_data_stream.save_to_wave_file(audio_stream)
            audio_stream.seek(0)
            audio_base64 = base64.b64encode(audio_stream.read()).decode('utf-8')
            return audio_base64
        else:
            print(f"Erro ao sintetizar áudio: {result.reason}")
            return None
    except Exception as e:
        print(f"Erro ao converter texto em áudio com Azure Speech: {e}")
        return None

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html', responses=responses)

if __name__ == '__main__':
    app.run(debug=True)
