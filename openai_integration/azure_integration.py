import azure.cognitiveservices.speech as speechsdk

def synthesize_speech(text):
    # Chave e região da sua assinatura da Azure
    api_key = "d00ed40fcc144be0a167721cf5867bee"
    region = "westeurope"

    # Configuração do serviço de fala da Azure
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)

    # Configuração de saída de áudio para a fala sintetizada
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # Inicializa o sintetizador de fala
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    try:
        # Sintetiza o texto fornecido em fala
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # URL temporário para a reprodução do áudio
            audio_url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
            return audio_url

        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")

    except Exception as ex:
        print(f"Speech synthesis failed: {ex}")

    return None
