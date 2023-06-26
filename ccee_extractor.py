import time 
import requests
import os
from src.Boto3Controller import S3Api
from urllib.parse import unquote
from requests import RequestException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def lambda_handler(event= None, context= None) -> dict:

    """Upload an object to an S3 bucket
    Payload exemple
    {
        "url"         : "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal",
        "profile"     : "default",
        "search_file" : "InfoMercado_Dados_Individuais"
    }
    """
    
    url         = event['url']
    profile     = event['profile']
    search_file = event['search_file']
    
    ### Start - Selenium WebScraping

    print("Etapa 1 - Abrir ChromeDrive")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/opt/headless-chromium"

    # pass the defined options and executable_path to initialize the web driver 
    driver = webdriver.Chrome(executable_path='/opt/chromedriver', chrome_options=options) 

    print("Etapa 2 - Requisição no ChromeDrive com URL")

    driver.get(url)
    time.sleep(10)

    print("Etapa 3 - Localizar elementos")

    # Find in HTML the desired element 
    content = driver.find_element(By.CSS_SELECTOR, "div[class*='list-documentos d-flex flex-wrap pr-2 pl-2'")
    links = content.find_elements(By.TAG_NAME, "a")

    # Loop through the href elements, searching for the desired pattern
    for item in links:
        if search_file in item.get_attribute("href"):
            link = item.get_attribute("href")
    
    # Return Status_Code 404 if can't find the element 
    if link is None:
        return {
            'status_code': 404,
            'body' : "Nenhum arquivo localizado"
        }

    print("Etapa 4 - Fechar o ChromeDrive")

    driver.close()
    driver.quit()

    ### End - Selenium WebScraping

    print("Etapa 5 - Fazer Download do arquivo")

    # Open Requests session to Download the file  
    session = requests.Session()

    try:
        response = session.get(link)
    except RequestException as e:
        return {
            'status_code' : 400,
            'body' : e
        }

    print("Etapa 6 - Enviar arquivo para Bucket S3")

    if response.status_code == 200:

        nome_arquivo = unquote(response.headers['Content-Disposition'].split('filename=')[1]).strip('\'"')
        caminho_arquivo = os.path.join('./', nome_arquivo)

        awsconn = S3Api(profile=profile)

        upload_response = awsconn.upload_s3_object(
            content=response.content,
            bucket='webscrapingstudy',
            folder='ccee', 
            filename=nome_arquivo
        )

        print("Arquivo salvo com sucesso")
    else:
        print("A requisição falhou com o código de status:", response.status_code)
        
        return {
            'status_code' : 400,
            'body' : 'A requisição falhou'
        }

    print("Etapa 7 - Fim da execução")

    return {
        'status_code' : 200,
        'body' : 'Arquivo salvo com sucesso'
    }