import requests

def get():
    url = 'http://192.168.76.129:8080/historicoAiExperience/get'

    headers = {}

    json = {}

    response = requests.get(url=url, json=json, headers=headers)
    response_data = str(response.json())
    string_response = response_data.replace("'","\"").replace("]","").replace("[","").replace("None", "null")  
    print(string_response) 
    return string_response

def postFrases(nome, frase):
    url = 'http://192.168.76.129:8080/historicoAiExperience/postFrases'

    headers = {}

    json = {
        "nome" : nome,
        "frase": frase
    }

    response = requests.post(url=url, json=json, headers=headers)

if __name__ == '__main__':
    #get()
    postFrases("Matheus Verna", "Imagino um futuro dominado por robos, e os humanos morando em marte.")