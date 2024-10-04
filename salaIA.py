import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import threading
import time
import processamentoIA
import pygame
import api
import json

class AplicacaoComVideo:
    def __init__(self, root, caminho_video, caminho_audio):
        self.root = root
        self.root.title("SALA IA")
        self.root.attributes("-fullscreen", True)  # Tela cheia

        # Configurar vídeo
        self.caminho_video = caminho_video
        self.cap = cv2.VideoCapture(caminho_video)
        self.largura = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.altura = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Criar um label para exibir o vídeo
        self.label_video = Label(root)
        self.label_video.pack(fill="both", expand=True)
        self.label_clique = tk.Label(root, text="Clique no Botão, e diga seu nome para iniciar...", font=("Helvetica", 50), background="white")
        self.label_clique.place(relx=0.5, rely=0.5, anchor="center")

        # Flag para controle do vídeo
        self.exibir_video = True
        # Flag para controlar a execução do método ia
        self.executando_ia = False

        # Inicializar o Pygame para reprodução de áudio
        pygame.mixer.init()
        self.caminho_audio = caminho_audio
        self.volume = 0.2
        pygame.mixer.music.set_volume(self.volume)

        # Atualizar frames do vídeo
        self.atualizar_frame()

        # Adicionar um evento para atualizar a posição do Label ao redimensionar a janela
        self.root.bind("<Configure>", self.atualizar_posicao_label)

        # Iniciar a música de fundo em uma thread separada
        threading.Thread(target=self.tocar_musica_fundo, daemon=True).start()

        # Iniciar a verificação contínua da flag status
        self.consultar_api_continuamente()

    def atualizar_frame(self):
        if self.exibir_video:
            ret, frame = self.cap.read()
            if not ret:
                # Reiniciar o vídeo quando ele termina
                self.cap.release()
                self.cap = cv2.VideoCapture(self.caminho_video)
                ret, frame = self.cap.read()
            if ret:
                # Converter o frame para o formato adequado
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.root.winfo_width(), self.root.winfo_height()))
                imagem = Image.fromarray(frame)
                imagem_tk = ImageTk.PhotoImage(image=imagem)

                # Atualizar o label do vídeo
                self.label_video.imgtk = imagem_tk
                self.label_video.configure(image=imagem_tk)

        self.root.after(20, self.atualizar_frame)  # Atualiza a cada 20 milissegundos

    def atualizar_posicao_label(self, event=None):
        # Atualizar a posição do Label para o centro da tela
        self.label_clique.place(relx=0.5, rely=0.5, anchor="center")

    def consultar_api_continuamente(self):
        # Consultar a API em intervalos regulares
        self.root.after(1000, self.verificar_status)  # Verifica a cada 1 segundo

    def verificar_status(self):
        if not self.executando_ia:  # Só consulta a API se o ia não estiver rodando
            threading.Thread(target=self.inicio).start()
        self.consultar_api_continuamente()  # Continuar verificando após cada execução

    def inicio(self):
        try:
            data = json.loads(api.get())
            status = data.get("status", 0)
            if status == 1 and not self.executando_ia:  # Se o status for 1 e ia não está rodando
                self.executando_ia = True  # Definir que ia está em execução
                self.tarefa_botao()
        except Exception as e:
            # Em caso de erro, você pode adicionar um log ou mensagem para depuração
            print(f"Erro ao consultar API: {e}")

    def tarefa_botao(self):
        # Executa o método ia e, ao terminar, libera a flag
        threading.Thread(target=self.ia).start()

    def mostrar_timer(self, segundos):
        if segundos > 0:
            self.label_clique.config(text=f"{segundos}", font=("Helvetica", 300))
            self.root.after(1000, self.mostrar_timer, segundos - 1)
        else:
            self.label_clique.config(text="")
            # Voltar a exibir o vídeo
            self.exibir_video = True

    def mostrar_nome(self, nome):
        self.label_clique.config(text="Olá, " + nome + "!", font=("Helvetica", 100))

    def tocar_musica_fundo(self):
        """Toca a música de fundo em loop."""
        try:
            pygame.mixer.music.load(self.caminho_audio)
            pygame.mixer.music.play(-1)  # -1 para tocar em loop
            print("Música de fundo tocando...")
            while True:  # Manter a thread em execução
                pygame.time.Clock().tick(10)
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar a música: {e}")

    def ia(self):
        try:
            self.mostrar_timer(5)
            processamentoIA.gravar_audio(5, "nome.wav")
            print("Audio finalizado")
            texto = processamentoIA.converterAudioTexto("nome.wav")
            print("Conversão finalizada")
            nome = texto.text.replace(".", "")
            self.mostrar_nome(nome)

            # Iniciar áudio e processos de IA
            self.reproduzir_audio('Audio/introducao.mp3')
            time.sleep(31)
            self.mostrar_timer(10)
            time.sleep(11)

            self.reproduzir_audio('Audio/gravacao.mp3')
            time.sleep(16)
            self.mostrar_timer(20)

            processamentoIA.gravar_audio(20, "gravacao.wav")
            print("Audio finalizado")
            texto = processamentoIA.converterAudioTexto("gravacao.wav")
            print("Conversão finalizada")

            self.reproduzir_audio('Audio/desenvolvimento.mp3')

            # Exibir imagem gerada
            imagem = processamentoIA.criacaoImagem(texto)
            imagem = imagem.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            imagem_tk = ImageTk.PhotoImage(imagem)
            self.exibir_video = False
            self.label_video.configure(image=imagem_tk)
            self.label_video.imgtk = imagem_tk
            time.sleep(15)

            self.reproduzir_audio('Audio/finalizacao.mp3')
            time.sleep(23)

            api.postFrases(nome, texto.text)
        finally:
            self.label_clique.config(text="")
            self.exibir_video = True
            self.executando_ia = False  # Libera a flag para voltar a consultar a API

    def reproduzir_audio(self, caminho_audio):
        """Reproduz um áudio específico sem parar a música de fundo."""
        canal = pygame.mixer.Channel(1)  # Usar um canal separado
        canal.set_volume(0.8)  # Ajustar volume se necessário
        canal.play(pygame.mixer.Sound(caminho_audio))
    


# Função para inicializar a aplicação
def iniciar_aplicacao():
    root = tk.Tk()
    app = AplicacaoComVideo(root, "Imagem/Tunnel.mp4", "Audio/musicaAmbiente.mp3")
    root.mainloop()

# Executar a aplicação
if __name__ == "__main__":
    iniciar_aplicacao()
