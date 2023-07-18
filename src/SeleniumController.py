import os
import time
import requests
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service

class SeleniumDriver:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, driver_path:str=None, binary_path:str=None, download_path:str=None):
        
        """SeleniumDriver constructor, returns a headless Webdriver instance

        :param driver_path (Optional): Browser driver path
        :param download_path (Optional): Download folder path
        """
        prefs = {
            'download.default_directory': download_path
        }

        self.driver = None
        self.driver_path = driver_path if driver_path is not None else None
        self.binary_path = binary_path if binary_path is not None else None
        self.prefs = prefs if download_path is not None else None

        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("prefs", self.prefs)
        options.binary_location = self.binary_path

        self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)

        #service = Service(executable_path=self.driver_path)
        #self.driver = webdriver.Chrome(service=service, options=options)
            
    def get_session(self):

        return self.driver
    
    def download_files_selenium(self, download_url:str):

        """Download a file from indicated URL with Selenium

        :param download_url (Optional): Download URL
        """

        try:
            self.driver.get(download_url)
            time.sleep(10)
        except Exception as e:
            print("Erro ao realizar o download: " + str(e))

        files = os.listdir(self.download_path)
        for file_name in files:
            if os.path.isfile(os.path.join(self.download_path, file_name)):
                filename = file_name

        return filename

    def download_files_requests(self, download_path:str, download_url:str):

        """Download a file from indicated URL with Requests

        :param download_url (Optional): Download URL
        """

        session = requests.Session()

        try:
            response = session.get(download_url)
            filename = response.headers['Content-Disposition'].split("filename=")[-1].strip("\"'")
        except Exception as e:
            print("Erro ao realizar o download: " + str(e))

        if response.status_code == 200:
            filepath = os.path.join(download_path, filename)

            with open(filepath, 'wb') as file:
                file.write(response.content)

            print("Arquivo baixado com sucesso:", filename)

            result = filename
        else:
            print("Falha ao baixar o arquivo.")

            result = False

        return result