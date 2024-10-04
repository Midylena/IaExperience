from openai import OpenAI
from PIL import Image
from io import BytesIO
import requests
import os
import pyaudio
import wave

client = OpenAI(api_key="sk-proj-TrfcTUJGxlJPLEerexhxT3BlbkFJViPPPn8m2yYbxQdHBlES",
                organization="org-xJfOKoKf4Vhg5dwFpExxNPPc")

def gravar_audio(duracao, nome_arquivo):
    # Configurações de áudio
    formato = pyaudio.paInt16  # Formato de áudio (16 bits)
    canais = 1  # Número de canais (mono)
    taxa_amostragem = 44100  # Taxa de amostragem (44.1 kHz)
    tamanho_buffer = 1024  # Tamanho do buffer

    # Inicializa a interface PyAudio
    p = pyaudio.PyAudio()

    # Abre o stream de áudio
    stream = p.open(format=formato,
                    channels=canais,
                    rate=taxa_amostragem,
                    input=True,
                    frames_per_buffer=tamanho_buffer)

    print("Gravando...")

    # Armazena os frames de áudio
    frames = []

    # Captura o áudio do microfone
    for _ in range(0, int(taxa_amostragem / tamanho_buffer * duracao)):
        data = stream.read(tamanho_buffer)
        frames.append(data)

    print("Gravação finalizada!")

    # Para e fecha o stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salva o áudio em um arquivo .wav
    with wave.open(nome_arquivo, 'wb') as wf:
        wf.setnchannels(canais)
        wf.setsampwidth(p.get_sample_size(formato))
        wf.setframerate(taxa_amostragem)
        wf.writeframes(b''.join(frames))


def converterAudioTexto(audio):

    audio_file= open(audio, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file)

    return transcription

def criacaoImagem(texto):

    prompt = "Frase: '"+texto.text+"""' Crie uma imagem realística e dramática que represente a percepção da FRASE acima. 
Faça essa imagem no formato adequado para ultrawide com distorção angular de 180º"""

    print(prompt)

    print("Carregando Imagem...")

    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    quality="standard",
    n=1)


    image_url = response.data[0].url

    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))

    if not os.path.exists("Imagem"):
        os.makedirs("Imagem")

    # Caminho completo do arquivo
    caminho_arquivo = os.path.join("Imagem", "imagem.png")

    # Salvar a imagem
    img.save(caminho_arquivo)
    print("Imagem Gerada!")

    return img

#gravar_audio(10,"gravacao.wav")
#criacaoImagem(converterAudioTexto("gravacao.wav")).show()