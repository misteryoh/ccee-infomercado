from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumBrowser:

    def __init__(self, driver_path=None):
        """Selenium Browser Controller to reuse common libs patterns

        :param: driver_path: string
        """

        self.driver_path = driver_path
        self.driver = None

    def session(self) -> Chrome:
        """Open Chrome Browser Session with options config --headless

        :return: Chrome(WebDriver)
        """

        # start by defining the options 
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = "/opt/headless-chromium"

        # normally, selenium waits for all resources to download 
        # we don't need it as the page also populated with the running javascript code. 
        options.page_load_strategy = 'none' 

        # this returns the path web driver downloaded 
        if self.driver_path is None:
            driver_path = ChromeDriverManager().install()
            browser_service = Service(driver_path) 
        else:
            browser_service = Service(self.driver_path)

        # pass the defined options and service objects to initialize the web driver 
        self.driver = Chrome(options=options, service=browser_service) 
        self.driver.implicitly_wait(5)

        return self.driver