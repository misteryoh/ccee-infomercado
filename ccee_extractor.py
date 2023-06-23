import time 
import requests
import os
from urllib.parse import unquote
from requests import RequestException
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

def lambda_handler(event= None, context= None) -> dict:

    url = "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal" 
    
    driver = selenium_session()
    driver.get(url)

    time.sleep(10)

    content = driver.find_element(By.CSS_SELECTOR, "div[class*='list-documentos d-flex flex-wrap pr-2 pl-2'")
    #link = content.find_element(By.TAG_NAME, "a").get_attribute("href")

    links = content.find_elements(By.TAG_NAME, "a")

    for item in links:
        if "InfoMercado_Dados_Individuais" in item.get_attribute("href"):
            link = item.get_attribute("href")
    
    if link is None:
        return {
            'status_code': 400,
            'body' : "Nenhum arquivo localizado"
        }
            
    session = requests.Session()

    try:
        response = session.get(link)
    except RequestException as e:
        return {
            'status_code' : 400,
            'body' : e
        }

    if response.status_code == 200:

        nome_arquivo = unquote(response.headers['Content-Disposition'].split('filename=')[1]).strip('\'"')
        caminho_arquivo = os.path.join('./', nome_arquivo)

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(response.content)

        print("Arquivo salvo com sucesso")
    else:
        print("A requisição falhou com o código de status:", response.status_code)
        
        return {
            'status_code' : 400,
            'body' : 'A requisição falhou'
        }

    return {
        'status_code' : 200,
        'body' : 'Arquivo salvo com sucesso'
    }

def selenium_session() -> Chrome:
    # start by defining the options 
    options = webdriver.ChromeOptions() 
    options.add_argument('--headless')

    # normally, selenium waits for all resources to download 
    # we don't need it as the page also populated with the running javascript code. 
    options.page_load_strategy = 'none' 

    # this returns the path web driver downloaded 
    chrome_path = ChromeDriverManager().install() 
    chrome_service = Service(chrome_path) 

    # pass the defined options and service objects to initialize the web driver 
    driver = Chrome(options=options, service=chrome_service) 
    driver.implicitly_wait(5)

    return driver

lambda_handler()