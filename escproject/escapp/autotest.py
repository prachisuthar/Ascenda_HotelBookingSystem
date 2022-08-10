from random import randint
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

def sleep_quit (n=3):
    time.sleep(n)
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

def scroll_and_click(button_id):
    button = driver.find_element(By.ID, button_id)
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(1)
    actions = ActionChains(driver)
    actions.move_to_element(button)
    actions.click()
    actions.perform()

def signup (fullname, email, username, password, confirm_password):
    driver.find_element(By.NAME, "full_name").send_keys(fullname)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "confirm_password").send_keys(confirm_password)

    scroll_and_click('signup_button')

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
  

def full_booking_run():
    # driver = webdriver.Chrome(PATH)
    driver.get(url)
    go_to_page("login")
    login("testerman", "testerman")
    time.sleep(1)
    search("Singapore, Singapore", "18092022", "19092022", "2", "2")
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
    # driver = webdriver.Chrome(PATH)
    driver.get(url)
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

def book_with_signup():
    go_to_page("signup")
    signup("tester tester", "testertester@gmail.com", "tester123", "tester123", "tester123")
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

# book_with_signup()
# full_booking_run()
# book_without_login()

###---------------------------Fuzzing---------------------------###
characters = "!@#$%^&*()_+}{|:<>'?~`/"
letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"

def flipABit(valid_input=""):
    randchar = randint(0, len(characters)-1)
    randpos = randint(0, len(valid_input)-1)

    return valid_input[:randpos] + characters[randchar] + valid_input[randpos+1:]

def trim(valid_input=""):
    randpos = randint(0, len(valid_input)-1)
    return valid_input[:randpos]

def insertChar(valid_input=""):
    randchar = randint(0, len(characters)-1)
    return valid_input + characters[randchar]

def rand_punctuation(n=7):
    rand_punctuation = ""
    for i in range(n):
        randchar = randint(0, len(characters)-1)
        rand_punctuation += characters[randchar]
    return rand_punctuation

def randword(n=7):
    randword = ""
    for i in range(n):
        randletter = randint(0, len(letters)-1)
        randword += letters[randletter]
    return randword

def randnum(n=4):
    randnum = ""
    for i in range(n):
        rand = randint(0, len(numbers)-1)
        randnum += numbers[rand]
    return randnum

def fuzz_search():
    destination = rand_punctuation(9)
    start = randnum(8)
    end = randnum(8)
    rooms = randnum(1)
    guests = randnum(1)
    search(destination, start, end, rooms, guests)
    sleep_quit()

def fuzz_signup():
    go_to_page("signup")
    full_name = rand_punctuation(10)
    email = trim("testerman@gmail.com")
    username = full_name
    password = rand_punctuation(8)
    confirm_password = rand_punctuation(8)
    signup(full_name, email, username, password, confirm_password)
    sleep_quit()

def fuzz_login():
    go_to_page("login")
    username = rand_punctuation(10)
    password = rand_punctuation(8)
    login(username, password)
    sleep_quit()

def fuzz_booking():
    go_to_page("login")
    login("testerman", "testerman")
    search("Singapore, Singapore", "18092022", "19092022", "2", "2")
    time.sleep(1)
    driver.find_element(By.ID, "view_button").click()
    time.sleep(1)
    scroll_and_click("rooms_button")
    time.sleep(1)
    driver.find_element(By.ID, "book_button").click()
    time.sleep(1)
    driver.find_element(By.ID, "payment_button").click()
    book(randword(8), randword(3), randnum(8), insertChar("testerman@gmail.com"), rand_punctuation(14), randnum(16), flipABit("8 somapah rd"), randnum(3), randnum(4))
    time.sleep(1)
    driver.find_element(By.ID, "confirm_transaction_button").click()
    sleep_quit()

fuzz_search()
# fuzz_signup()
# fuzz_login()
# fuzz_booking()
###---------------------------Fuzzing---------------------------###


