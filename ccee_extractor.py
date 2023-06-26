import time 
import requests
import os
from src.SeleniumController import SeleniumBrowser
from src.Boto3Controller import S3Api
from urllib.parse import unquote
from requests import RequestException
from selenium.webdriver.common.by import By 

def lambda_handler(event= None, context= None) -> dict:

    """Upload an object to an S3 bucket
    Payload exemple
    {
        "url"         : "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal",
        "driver_path" : "/opt/driver/chromedriver",
        "profile"     : "default",
        "search_file" : "InfoMercado_Dados_Individuais"
    }
    """
    
    url         = event['url']
    driver_path = event['driver_path']
    profile     = event['profile']
    search_file = event['search_file']
    
    # Instance Selenium Browser - Chrome
    # browser = SeleniumBrowser()
    browser = SeleniumBrowser(driver_path=driver_path) # Use for lambda layer with chromedriver
    driver = browser.session()
    driver.get(url)
    time.sleep(10)

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

    # Open Requests session to Download the file  
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

    return {
        'status_code' : 200,
        'body' : 'Arquivo salvo com sucesso'
    }