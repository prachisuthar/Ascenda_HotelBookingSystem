from django.test import TestCase

# Create your tests here.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
# from selenium.webdriver.common.keys import Keys

PATH = "/Users/keshavnatarajan/Documents/SUTD/Term 5/Software Construction/Testing/chromedriver"
url = "http://127.0.0.1:8000/"

driver = webdriver.Chrome(PATH)
driver.get(url)

print(driver.title)
# print(driver.page_source)

def sleep_quit ():
    time.sleep(5)
    driver.quit()

def go_to_page(page_id):
    if page_id == "login":
        search = driver.find_element(By.CSS_SELECTOR, 'a[href*="login"]')
        print(search)
        search.click()
    elif page_id == "signup":
        search = driver.find_element(By.CSS_SELECTOR, 'a[href*="signup"]')
        search.click()
    elif page_id == "booking":
        search = driver.find_element_by_id(By.CSS_SELECTOR, 'a[href*="booking"]')
        search.click()


def signup (username, password, fullname, confirm_password):
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "full_name").send_keys(fullname)
    driver.find_element(By.NAME, "confirm_password").send_keys(confirm_password)

    driver.find_element(By.ID, 'signup_button').click()

def login (username, password):
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.ID, "login_button").click()

def book(first_name, last_name, phone_number, email, request, card_no, billing, cvv, expiry):
    driver.find_element(By.NAME, "first_name").send_keys(first_name)
    driver.find_element(By.NAME, "last_name").send_keys(last_name)
    driver.find_element(By.NAME, "phone_number").send_keys(phone_number)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "request").send_keys(request)
    driver.find_element(By.NAME, "credit_card_no").send_keys(card_no)
    driver.find_element(By.NAME, "billing_address").send_keys(billing)
    driver.find_element(By.NAME, "cvv").send_keys(cvv)
    driver.find_element(By.NAME, "expiry").send_keys(expiry)

    driver.find_element(By.ID, "book_button").click()

# test case 1
def regular_signup():
    go_to_page("signup")
    signup("test", "test_password", "tester", "test_password")
    sleep_quit()

# test case 2
def signup_password_mismatch():
    go_to_page("signup")
    signup("test", "test_password", "tester", "different_password")
    sleep_quit()

# test case 3
def regular_login():
    go_to_page("login")
    login("test", "test_password")
    sleep_quit()

# test case 4
def wrong_user_login():
    go_to_page("login")
    login("test1234", "test_password")
    sleep_quit()

# test case 5
def wrong_password_login():
    go_to_page("login")
    login("test", "wrong_password")
    sleep_quit()

# test case 6
def incorrect_phone_number():
    go_to_page("booking")
    book("bob", "tan", "123", "bob_tan@gmail.com", "NA", "8564734583491234", "8 somapah rd", "123", "523")
    sleep_quit()

# test case 7
def credit_card_many_numbers():
    go_to_page("booking")
    book("bob", "tan", "98463923", "bob_tan@gmail.com", "NA", "8564734583491232342345234", "8 somapah rd", "123", "523")
    sleep_quit()  

# test case 8
def invalid_email():
    go_to_page("booking")
    book("bob", "tan", "98463923", "bob_tan@@gmail.com", "NA", "8564734583491234", "8 somapah rd", "123", "523")
    sleep_quit() 



regular_login()





"""
country = "Singapore"
start_date = "03-02-2022"
end_date = "03-06-2022"
guests_number ="5"
rooms_number ="2"

driver.find_element(By.NAME,"country").send_keys(country)
driver.find_element("name","start_date").send_keys(start_date)
driver.find_element("name","end_date").send_keys(end_date )
driver.find_element("name","guests_number").send_keys(guests_number)
driver.find_element("name","rooms_number").send_keys(rooms_number)
#driver.find_element(By.X.PATH, "button").click()
#transfer_input = driver.element_to_be_clickable((By.XPATH, 'button'))
#transfer_input.click()
# button = driver.find_element_by_css_selector('button')
# button.click()
#driver.find_elements(By.XPATH, 'button').click()
driver.find_element(By.ID, 'button').click()
driver.find_element("name","a").click()    
"""

"""
from django.test import TestCase
# import django
import os
import sys

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "escapp.escproject.settings")
# django.setup()
# Create your tests here.
# from .models import Customer
# from . import models
from .models import Customer
# import models.Customer


# class Feature1TestCase(TestCase):
#     def test_feature1_exists(self):
#         qs = Feature1.objects.all()  #taking all teh objects and check if it exists
#         self.assertTrue(qs.exists())

class CustomerTestCase(self):
    self.customer = Customer.objects.create(full_name='aish')
    self.assertEquals(str(self.customer),'aish')
"""

from django.urls import reverse
from escapp.models import *


# class BaseTest(TestCase):
#     def setUp(self):
#         self.signup_url=reverse('signup.html')
#         return super().setUp()

# test case 1

class BaseTest(TestCase):
    def setUp(self):
        self.signup_url=reverse('escapp:signup')
        self.login_url=reverse('escapp:login')
        self.booking_url=reverse('escapp:booking')
        self.signup={
            'username': 'test2',
            'password': 'test_password',
            'full_name': 'tester',
            'confirm_password': 'test_password'
        }
        self.password_mismatch={
            'username': 'test3',
            'password': 'test_password',
            'full_name': 'tester',
            'confirm_password': 'wrong_password'
        }
        self.login={
            'username': 'test2',
            'password': 'test_password',
        }
        self.incorrect_credentials={
            'username': 'test2',
            'password': 'wrong_password',
        }
        self.booking={
            'first_name': 'bob',
            'last_name': 'tan',
            'phone_number': '83245344',
            'email': 'bob_tan@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }

        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_can_register_user(self):
        response=self.client.post(self.signup_url,self.signup,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_username_exists(self):
        response=self.client.post(self.signup_url,self.password_mismatch,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_can_login(self):
        response=self.client.post(self.login_url,self.login,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_credentials(self):
        response=self.client.post(self.login_url,self.incorrect_credentials,format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_can_book(self):
        response=self.client.post(self.booking_url,self.booking,format='text/html')
        self.assertEqual(response.status_code, 200)

    



# class Feature1TestCase(TestCase):
#     def test_feature1_exists(self):
#         qs = Feature1.objects.all()  #taking all the objects and check if it exists
#         self.assertTrue(qs.exists())

# class CustomerTestCase(self):
#     self.customer = Customer.objects.create(full_name='aish')
#     self.assertEquals(str(self.customer),'aish')
