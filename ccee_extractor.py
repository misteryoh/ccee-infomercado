import time 
import requests
import os
from src.Boto3Controller import S3Api
from src.SeleniumController import SeleniumDriver
from urllib.parse import unquote
from requests import RequestException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def lambda_handler(event= None, context= None) -> dict:

    """Upload an object to an S3 bucket
    """
    
### Parameters definition

    url         = "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal"
    driver_path = "/home/misteryoh/Coding/Git/ccee-infomercado/chrome-driver/chrome2018/chromedriver"
    binary_path = "/home/misteryoh/Coding/Git/ccee-infomercado/chrome-driver/chrome2018/headless-chromium"
    download_path = "/home/misteryoh/Coding/Git/ccee-infomercado/data/"
    profile     = "default"
    
### Start - Selenium WebScraping

    print("Step 1 - Open ChromeDrive")

    browser = SeleniumDriver(driver_path=driver_path, binary_path=binary_path, download_path=download_path)

    print("Step 2 - Request at the URL")

    browser.driver.get(url)
    #time.sleep(10)

    print("Step 3 - Search the desire elements")

    # Find in HTML the desired element 
    content = browser.driver.find_element(By.CSS_SELECTOR, "div[class*='list-documentos d-flex flex-wrap pr-2 pl-2'")
    links = content.find_elements(By.TAG_NAME, "a")

    # Loop through the href elements, searching for the desired pattern
    for item in links:
        if 'InfoMercado' in item.get_attribute("href") and 'Individuais' in item.get_attribute("href"):
            link = item.get_attribute("href")
    
    # Return Status_Code 404 if can't find the element 
    if link is None:
        return {
            'status_code': 404,
            'body' : "Nenhum arquivo localizado"
        }

    print("Step  4 - Download File")
    
    try:
        browser.driver.get(link)
        time.sleep(10)
    except Exception as e:
        print("Erro ao realizar o download: " + str(e))

    browser.driver.close()
    browser.driver.quit()

### End - Selenium WebScraping

### Start - Struct Data



### End - Struct Data

    print("Etapa 6 - Enviar arquivo para Bucket S3")

    nome_arquivo = unquote(response.headers['Content-Disposition'].split('filename=')[1]).strip('\'"')
    caminho_arquivo = os.path.join('./', nome_arquivo)

    awsconn = S3Api(profile=profile)

    upload_response = awsconn.upload_s3_object(
        content=response.content,
        bucket='webscrapingstudy',
        folder='ccee', 
        filename=nome_arquivo
    )

    print("Etapa 7 - Fim da execução")

    return {
        'status_code' : 200,
        'body' : 'Arquivo salvo com sucesso'
    }

lambda_handler()