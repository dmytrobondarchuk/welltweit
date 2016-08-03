import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from user_info import user_name, user_password, full_user_name

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
        print ('User page is succesfully loaded')

    def get_logined_user_name(self):

        self.logined_user_name = WebDriverWait(self.driver, 10).until(
                                    ec.presence_of_element_located((By.CSS_SELECTOR, '.user-name'))).text
        print ('User loginned as', self.logined_user_name)

        return self.logined_user_name



class TestLogin(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Firefox()
        self.driver.get('http://test.azure.welltweit.com/')
        self.driver.implicitly_wait(4)

    def tearDown(self):
        print ("END OF THE TEST")
        self.driver.close()


    def test_valid_login(self):
        '''User tries login using valid name and password'''             
        home_page = HomePage(self.driver)
        user_home_page = home_page.login(user_name, user_password)
        user_home_page.print_status()
        assert full_user_name in user_home_page.get_logined_user_name()

if __name__ == '__main__':
    unittest.main()