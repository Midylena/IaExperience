from openai import OpenAI
client = OpenAI(api_key="sk-proj-TrfcTUJGxlJPLEerexhxT3BlbkFJViPPPn8m2yYbxQdHBlES",
                organization="org-xJfOKoKf4Vhg5dwFpExxNPPc")

audio_file= open("gravacao.wav", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)