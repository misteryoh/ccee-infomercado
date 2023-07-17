import time 
import os
import resource
from urllib.parse import unquote
from src.Boto3Controller import S3Api
from src.SeleniumController import SeleniumDriver
from src.SheetController import SheetData
from selenium.webdriver.common.by import By


def lambda_handler(event= None, context= None) -> dict:

    """Upload an object to an S3 bucket
    """

### Parameters definition

    url         = "https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal"
    driver_path = "/home/misteryoh/Coding/Git/ccee-infomercado/chrome-driver/2020/chromedriver"
    binary_path = "/home/misteryoh/Coding/Git/ccee-infomercado/chrome-driver/2020/headless-chromium"
    download_path = "/home/misteryoh/Coding/Git/ccee-infomercado/data/"
    profile     = "default"

    params = [
        {
            "sheet_name"      : "002 Usinas",
            "table_name"      : "Tabela 001",
            "first_col"       : "Código do Ativo",
            "last_col"        : "Geração por Unit Commitment",
            "footer"          : "Topo",
            "deadrows"        : 3,
            "output_name"     : "InfoMercado_Usinas",
            "output_type"     : ".csv"
        },
        {
            "sheet_name"      : "007 Lista de Perfis",
            "table_name"      : "Tabela 001",
            "first_col"       : "Cód. Agente",
            "last_col"        : "Perfil Varejista",
            "footer"          : "Topo",
            "deadrows"        : 2,
            "output_name"     : "InfoMercado_Perfis",
            "output_type"     : ".csv"
        }
    ]
    
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

    print("Step 4 - Download File")
    
    try:
        browser.driver.get(link)
        time.sleep(10)
    except Exception as e:
        print("Erro ao realizar o download: " + str(e))

    browser.driver.close()
    browser.driver.quit()

### End - Selenium WebScraping

### Start - Struct Data

    print("Step 5 - Get file and struct data")

    files = os.listdir(download_path)
    for file_name in files:
        if os.path.isfile(os.path.join(download_path, file_name)):
            filename = file_name
    
    struct_result = SheetData()
    struct_result = struct_result.load_workbook(filepath=download_path, filename=filename)
    struct_result = struct_result.extract_data(params)

### End - Struct Data

### Start - Upload Struct Data to AWS

    print("Step 6 - Upload files to S3 Bucket")

    awsconn = S3Api(profile=profile)

    for struct_data in struct_result:
        upload_response = awsconn.upload_s3_object(
            content=struct_data['data'],
            bucket='webscrapingstudy',
            folder='ccee', 
            filename=struct_data['file'] + struct_data['type']
        )

    print("Etapa 7 - Fim da execução")

    return {
        'status_code' : 200,
        'body' : 'Arquivo salvo com sucesso'
    }

### End - Upload Struct Data to AWS

lambda_handler()