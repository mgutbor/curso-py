import requests
from lxml import html

encabezados = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

url = "https://wikipedia.org/"

respuesta = requests.get(url, headers=encabezados)
respuesta.encoding = 'utf-8'

parseador = html.fromstring(respuesta.text)

idiomas = parseador.find_class('central-featured-lang')

for idioma in idiomas:
    print(idioma.text_content())