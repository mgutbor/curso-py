import requests
from bs4 import BeautifulSoup

encabezados = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

url = "https://stackoverflow.com/questions/"

respuesta = requests.get(url, headers=encabezados)
respuesta.encoding = 'utf-8'

soup = BeautifulSoup(respuesta.text)

contenedor = soup.find(id="questions")

listado_post = contenedor.find_all('div',class_="s-post-summary")

for post in listado_post:
    titulo_post = post.find('h3').text
    descripcion_post = post.find('div', class_="s-post-summary--content-excerpt").text.replace('\n', '').replace('\r', '').strip()
    print(titulo_post)
    print(descripcion_post)
    print("==================================================")

#test