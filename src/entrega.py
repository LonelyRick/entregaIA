import PyPDF2
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
from grobid_client.grobid_client import GrobidClient

# Conexión con API de Grobid
grobid_url = 'http://localhost:8070/api/processFulltextDocument'
headers = {'Accept': 'application/xml'}
client = GrobidClient(config_path="./config.json")

#Lista de PDFs a evaluar
pdfs = ['64602307.pdf', '39308_Inteligencia_artificial.pdf']

#Obtención del html mediante Grobid
def getGrobid(pdf):
    with open(pdf, 'rb') as file:
        reader = file.read()
        respuesta =client.post(grobid_url, headers=headers, files={'input': ('input.pdf', reader)})
        if str(respuesta[0]) == "<Response [200]>" : 
            fres = respuesta[0].text.encode("utf-8")
        else:
            print('Error:', respuesta[0])
        return str(fres)

#Obtención de abstracto
def getAbstract(respuesta):
    abstract = re.findall(r"<abstract>(.*?)</abstract>", respuesta, re.DOTALL)
    #print(abstract[0])
    cleanAbstract = re.sub('<.*?>', '', abstract[0]).strip()  
    cleanAbstract = cleanAbstract.encode('utf-8')  
    #print(cleanAbstract)
    return cleanAbstract

#Obtención de figuras
def getNumFigures(respuesta):
    figures = len(re.findall(r"<figure(.*?)</figure>", respuesta, re.DOTALL))
    return figures

#Obtención de links
def getLinks(respuesta):
    links = re.findall(r'<ptr target=(\S+)', respuesta, re.DOTALL)
    return links


#Generación de WordCloud
def getWordCloud(abstract):
    wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(abstract)
    return wordcloud

def pintar(wordcloud):
    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def grafica(figures, pfds):
    plt.figure()
    plt.bar(range(len(figures)), figures)
    plt.xticks(range(len(figures)), [pdf for pdf in pdfs])
    plt.xlabel('Paper')
    plt.ylabel('Number of Figures')
    plt.show()

def listado(links,pdf):
    print(f'Links found in {pdf} :')
    for link in links:
        print(link)

def main():
    num_figures = []
    for pdf in pdfs:
        respuesta = getGrobid(pdf)
        #print(respuesta)
        abstracto = getAbstract(respuesta)
        # print(abstracto)
        wordcloud = getWordCloud(str(abstracto))
        pintar(wordcloud)
        figures = getNumFigures(respuesta)
        num_figures.append(figures)
        # print(figures)
        links = getLinks(respuesta)
        # print(links)
        listado(links,pdf)

    #print(num_figures)
    #grafica(num_figures,pdfs)


if __name__ == '__main__':
    main()


