from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
# from selenium.webdriver.common.keys import Keys

PATH = "/Users/keshavnatarajan/Documents/SUTD/Term 5/Software Construction/Testing/chromedriver"
url = "http://127.0.0.1:8000/"

driver = webdriver.Chrome(PATH)
driver.get(url)

print(driver.title)
# print(driver.page_source)
# driver.quit() #COMMENT OUT WHEN DOING SELENIUM TESTING

def sleep_quit ():
    time.sleep(3)
    driver.quit()


def go_to_page(page_id):
    if page_id == "login":
        search = driver.find_element(By.CSS_SELECTOR, 'a[href*="login"]')
        print(search)
        search.click()
    elif page_id == "signup":
        search = driver.find_element(By.CSS_SELECTOR, 'a[href*="signup"]')
        search.click()
    # elif page_id == "booking":
    #     search = driver.find_element_by_id(By.CSS_SELECTOR, 'a[href*="booking"]')
    #     search.click()


def signup (fullname, email, username, password, confirm_password):
    driver.find_element(By.NAME, "full_name").send_keys(fullname)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirm_password").send_keys(confirm_password)

    driver.find_element(By.ID, 'signup_button').click()

def login (username, password):
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.ID, "login_button").click()

def scroll_and_click(button_id):
    button = driver.find_element(By.ID, button_id)
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(1)
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click()
    actions.perform()


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

    scroll_and_click("booking_button")
    

def search(country, startdate, enddate, guest, room):
    driver.find_element(By.ID, "country").send_keys(country)
    driver.find_element(By.ID, "start_date").send_keys(startdate)
    driver.find_element(By.ID, "end_date").send_keys(enddate)
    driver.find_element(By.ID, "guests_number").send_keys(guest)
    driver.find_element(By.ID, "rooms_number").send_keys(room)

    driver.find_element(By.ID, "submit_button").click() 

# test case 1
def regular_signup():
    go_to_page("signup")
    signup("tester man", "testerman@gmail.com", "testerman", "testerman", "testerman")
    sleep_quit()

# test case 2
def signup_password_mismatch():
    go_to_page("signup")
    signup("test", "test_password", "tester", "different_password")
    sleep_quit()

# test case 3
def regular_login():
    go_to_page("login")
    login("testerman", "testerman")
    time.sleep(2)
    # sleep_quit()

# test case 4
def wrong_user_login():
    go_to_page("login")
    login("test1234", "test_password")
    sleep_quit()

  

def full_booking_run():
    regular_login()
    search("Singapore, Singapore", "18092022", "19092022", "2", "2")
    time.sleep(1)
    driver.find_element(By.ID, "view_button").click()
    time.sleep(1)
    scroll_and_click("rooms_button")
    time.sleep(1)
    driver.find_element(By.ID, "book_button").click()
    time.sleep(1)
    driver.find_element(By.ID, "payment_button").click()
    book("tester", "man", "98766543", "testerman@gmail.com", "extra pillows please", "1111222233334444", "8 somapah rd", "123", "1124")
    time.sleep(1)
    driver.find_element(By.ID, "confirm_transaction_button").click()
    sleep_quit()

def book_without_login():
    search("Singapore, Singapore", "18092022", "19092022", "2", "2")
    time.sleep(1)
    driver.find_element(By.ID, "view_button").click()
    time.sleep(1)
    scroll_and_click("rooms_button")
    time.sleep(1)
    driver.find_element(By.ID, "book_button").click()
    time.sleep(1)
    driver.find_element(By.ID, "booking_login_button").click()
    time.sleep(1)
    login("testerman", "testerman")
    book("tester", "man", "98766543", "testerman@gmail.com", "extra pillows please", "1111222233334444", "8 somapah rd", "123", "1124")
    time.sleep(1)
    driver.find_element(By.ID, "confirm_transaction_button").click()

    sleep_quit()

# regular_signup()

full_booking_run()
# book_without_login()
# regular_login()