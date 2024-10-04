from openai import OpenAI
from PIL import Image
from io import BytesIO
import requests
import os

client = OpenAI(api_key="sk-proj-TrfcTUJGxlJPLEerexhxT3BlbkFJViPPPn8m2yYbxQdHBlES",
                organization="org-xJfOKoKf4Vhg5dwFpExxNPPc")

response = client.images.generate(
  model="dall-e-3",
  prompt="""Frase: "No futuro, acredito que carros vão voar, o clima será desértico e as pessoas serão corcundas." 
Crie uma imagem realística e dramática que represente a percepção da FRASE acima.
Faça essa imagem no formato adequado para ultrawide com distorção angular de 180º""",
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
print(f"Imagem salva em: {caminho_arquivo}")

img.show()