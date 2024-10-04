import pyaudio
import wave

def gravar_audio(duracao, nome_arquivo):
    # Configurações de áudio
    formato = pyaudio.paInt16  # Formato de áudio (16 bits)
    canais = 2  # Número de canais (mono)
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

    print("Gravação finalizada.")

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


# Exemplo de uso
duracao = 5  # Duração da gravação em segundos
nome_arquivo = "gravacao.wav"

gravar_audio(duracao, nome_arquivo)
print(f"Áudio salvo em: {nome_arquivo}")
