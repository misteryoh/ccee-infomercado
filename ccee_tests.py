import unittest
from unittest.mock import MagicMock
from ccee_extractor import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    def test_lambda_handler_success(self):
        event = {
            'url': 'https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal',
            'profile': 'default',
            'search_file': 'InfoMercado_Dados_Individuais'
        }
        
        # Mock the webdriver and requests.Session
        webdriver_mock = MagicMock()
        webdriver_mock.return_value.find_element.return_value = MagicMock()
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value = [MagicMock()]
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value[0].get_attribute.return_value = 'mocked_link'
        webdriver_mock.return_value.get.return_value = None
        
        requests_session_mock = MagicMock()
        requests_session_mock.return_value.get.return_value.status_code = 200
        requests_session_mock.return_value.get.return_value.headers = {'Content-Disposition': 'filename=test.txt'}
        requests_session_mock.return_value.get.return_value.content = b'mocked_content'
        
        with unittest.mock.patch('ccee_extractor.webdriver', webdriver_mock):
            with unittest.mock.patch('ccee_extractor.requests.Session', requests_session_mock):
                response = lambda_handler(event)
        
        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['body'], 'Arquivo salvo com sucesso')

    def test_lambda_handler_file_not_found(self):
        event = {
            'url': 'https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal',
            'profile': 'default',
            'search_file': 'Nonexistent_File'
        }
        
        # Mock the webdriver
        webdriver_mock = MagicMock()
        webdriver_mock.return_value.find_element.return_value = MagicMock()
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value = [MagicMock()]
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value[0].get_attribute.return_value = 'mocked_link'
        webdriver_mock.return_value.get.return_value = None
        
        with unittest.mock.patch('ccee_extractor.webdriver', webdriver_mock):
            response = lambda_handler(event)
        
        self.assertEqual(response['status_code'], 404)
        self.assertEqual(response['body'], 'Nenhum arquivo localizado')

    def test_lambda_handler_request_failed(self):
        event = {
            'url': 'https://www.ccee.org.br/dados-e-analises/dados-mercado-mensal',
            'profile': 'default',
            'search_file': 'InfoMercado_Dados_Individuais'
        }
        
        # Mock the webdriver and requests.Session
        webdriver_mock = MagicMock()
        webdriver_mock.return_value.find_element.return_value = MagicMock()
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value = [MagicMock()]
        webdriver_mock.return_value.find_element.return_value.find_elements.return_value[0].get_attribute.return_value = 'mocked_link'
        webdriver_mock.return_value.get.return_value = None
        
        requests_session_mock = MagicMock()
        requests_session_mock.return_value.get.side_effect = Exception('Request failed')
        
        with unittest.mock.patch('ccee_extractor.webdriver', webdriver_mock):
            with unittest.mock.patch('ccee_extractor.requests.Session', requests_session_mock):
                response = lambda_handler(event)
        
        self.assertEqual(response['status_code'], 400)
        self.assertIsInstance(response['body'], Exception)

if __name__ == '__main__':
    unittest.main()
