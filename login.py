import unittest
import HTMLTestRunner

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from user_info import user_name, user_password, full_user_name, wrong_password
from other_information import end_of_user_url, error_message

class HomePage(object):
    '''Home page with login fields'''

    def __init__(self, driver):
        self.driver = driver
        
    
    def login(self, user_name, user_password):
        ''' Login fields at the site '''

        user_name_field = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.ID,"LoginViewModel_Email")))
        user_name_field.send_keys(user_name)

        password_field = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.ID, "LoginViewModel_Password")))
        password_field.send_keys(user_password, Keys.ENTER)        
        
        return UserPage(self.driver)

class UserPage(object):
    '''User page which loads after successful login'''
    def __init__(self, driver):
        self.driver = driver

    def print_status(self):
        if end_of_user_url in self.driver.current_url:
            print ('User page is succesfully loaded')
        else:
            print ('User page is not loaded. User stayes at login page')

    def get_logined_user_name(self):

        self.logined_user_name = WebDriverWait(self.driver, 10).until(
                                    ec.presence_of_element_located((By.CSS_SELECTOR, '.user-name'))).text
        print ('User loginned as', self.logined_user_name)

        return self.logined_user_name
    
    def get_error_message(self):
        
        view_login_error_message = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_element_located((By.CLASS_NAME, "field-validation-error")))      
        text_to_return = view_login_error_message.text
        return text_to_return

class TestLogin(unittest.TestCase):

    def setUp(self):

        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(executable_path="/opt/chromedriver")
        self.driver.get('http://test.azure.welltweit.com/')
        self.driver.maximize_window()
        self.driver.implicitly_wait(4)

    def tearDown(self):
        #print ("END OF THE TEST")
        self.driver.close()

    #@unittest.skip('skips test of test_valid_login')
    def test_valid_login(self):
        '''User tries login using valid name and password'''             
        home_page = HomePage(self.driver)
        user_home_page = home_page.login(user_name, user_password)
        user_home_page.print_status()
        assert full_user_name in user_home_page.get_logined_user_name()

    def test_invalid_login(self):
        '''User tries login using invalid password'''             
        home_page = HomePage(self.driver)
        user_home_page = home_page.login(user_name, wrong_password)
        user_home_page.print_status()
        assert error_message in user_home_page.get_error_message()
        print (user_home_page.get_error_message())

if __name__ == '__main__':
    HTMLTestRunner.main()