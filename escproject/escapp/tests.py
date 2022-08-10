from multiprocessing.connection import Client
from random import randint
from django.test import TestCase
from django.urls import reverse
from escapp.models import *
from django.contrib.auth.models import User
from django.test import Client

##----------------Login Page----------------##
class LoginTestCase(TestCase):
    def setUp(self):
        self.login_url=reverse('escapp:login')
        self.signup_url=reverse('escapp:signup')

        self.password_mismatch={
            'username': 'test3',
            'password': 'wrong_password',
        }
        self.login={
            'username': 'testerman',
            'password': 'testerman',
        }
        self.incorrect_credentials={
            'username': 'test2',
            'password': 'wrong_password',
        }
        self.fuzzed_login={
            'username': Fuzzer().randword(5),
            'password': Fuzzer().randword(5),
        }
        self.fuzzed_jargon={
            'username': Fuzzer().rand_punctuation(5),
            'password': Fuzzer().rand_punctuation(5),
        }
        return super().setUp()

class LoginTest(LoginTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_username_exists(self):
        response=self.client.post(self.login_url,self.password_mismatch,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_can_login(self):
        response=self.client.post(self.login_url,self.login,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_credentials(self):
        response=self.client.post(self.login_url,self.incorrect_credentials,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzed_login(self):
        response=self.client.post(self.login_url,self.fuzzed_login,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzed_jargon(self):
        response=self.client.post(self.login_url,self.fuzzed_jargon,format='text/html')
        self.assertEqual(response.status_code, 200)

##------------------------------------------##

##----------------Signup Page----------------##
class RegisterTestCase(TestCase):
    def setUp(self):
        self.signup_url=reverse('escapp:signup')
        self.index_url=reverse('escapp:index')
        self.signup={
            'username': 'test2',
            'password': 'test_password',
            'email': 'tester@gmail.com',
            'full_name': 'tester',
            'confirm_password': 'test_password'
        }
        self.signup_new={
            'username': 'tester1235',
            'password': 'test_password1',
            'email': 'tester1235@gmail.com',
            'full_name': 'tester bester2',
            'confirm_password': 'test_password1'
        }
        self.wrong_password={
            'username': 'tester456',
            'password': 'test_password1',
            'email': 'tester125@gmail.com',
            'full_name': 'tester bester3',
            'confirm_password': 'wrongpassword'
        }
        self.existing_user={
            'username': 'tester456',
            'password': 'test_password2',
            'email': 'tester135@gmail.com',
            'full_name': 'tester bester4',
            'confirm_password': 'test_password2'
        }
        self.fuzzed={
            'username': 'tester456',
            'password': Fuzzer().rand_punctuation(8),
            'email': Fuzzer('tester135@gmail.com').trim(),
            'full_name': 'tester bester4',
            'confirm_password': Fuzzer().rand_punctuation(8)
        }
        self.fuzzed_username={
            'username': Fuzzer().rand_punctuation(5),
            'password': 'test_password1',
            'email': 'tester1235@gmail.com',
            'full_name': 'tester bester2',
            'confirm_password': 'test_password1'
        }
        self.fuzzed_password={
            'username': Fuzzer().randword(5),
            'password': Fuzzer().rand_punctuation(5),
            'email': 'tester1235@gmail.com',
            'full_name': 'tester bester2',
            'confirm_password': 'test_password1'
        }
        self.fuzzed_email={
            'username': Fuzzer().rand_punctuation(5),
            'password': 'test_password1',
            'email': Fuzzer('tester1235@gmail.com').insertChar(),
            'full_name': 'tester bester2',
            'confirm_password': 'test_password1'
        }
        return super().setUp()

class RegisterTest(RegisterTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_can_register_user(self):
        response=self.client.post(self.signup_url,self.signup,format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url=self.index_url, status_code=302)

    def test_can_register_user2(self):
        response=self.client.post(self.signup_url,self.signup_new,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_wrong_password(self):
        response=self.client.post(self.signup_url,self.wrong_password,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_existing_user(self):
        response=self.client.post(self.signup_url,self.existing_user,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_fuzzer_signup(self):
        response=self.client.post(self.signup_url,self.fuzzed,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_username(self):
        response=self.client.post(self.signup_url,self.fuzzed_username,format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_fuzzer_password(self):
        response=self.client.post(self.signup_url,self.fuzzed_password,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_email(self):
        response=self.client.post(self.signup_url,self.fuzzed_email,format='text/html')
        self.assertEqual(response.status_code, 200)
##-------------------------------------------##

##----------------Feature 1----------------##
class DestinationSearchTestCase(TestCase):
    def setUp(self):
        self.index_url=reverse('escapp:index')
        self.hotellist_url=reverse('escapp:hotellist')

        self.singapore_search={
            'country': 'Singapore, Singapore',
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '05012023',
            'end_date': '09012023',
        }
        self.kl_search={
            'country': 'Kuala Lumpur, Malaysia',
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '05/01/2023',
            'end_date': '09/01/2023',
        }
        self.rome_search={
            'country': 'Rome, Italy',
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '05/01/2023',
            'end_date': '09/01/2023',
        }
        self.wrong_date={
            'country': 'Singapore, Singapore',
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '09/01/2023',
            'end_date': '05/01/2023',
        }
        self.many_guests={
            'country': 'Singapore, Singapore',
            'guests_number': '8',
            'rooms_number': '1',
            'start_date': '05/01/2023',
            'end_date': '09/01/2023',
        }
        self.fuzzer={
            'country': Fuzzer('Singapore, Singapore').flipABit(),
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '05/01/2023',
            'end_date': '09/01/2023',
        }
        self.fuzzer_dest={
            'country': Fuzzer().rand_punctuation(12),
            'guests_number': '1',
            'rooms_number': '1',
            'start_date': '05/01/2023',
            'end_date': '09/01/2023',
        }
        self.fuzzer_all={
            'country': Fuzzer().rand_punctuation(12),
            'guests_number': Fuzzer().randnum(1),
            'rooms_number': Fuzzer().randnum(1),
            'start_date': Fuzzer().randnum(8),
            'end_date': Fuzzer().randnum(8),
        }
        return super().setUp()

class DestinationSearchTest(DestinationSearchTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_search_singapore_hotels(self):
        response=self.client.post(self.index_url,self.singapore_search,format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_search_kl_hotels(self):
        response=self.client.post(self.index_url,self.kl_search,format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_search_other_hotels(self):
        response=self.client.post(self.index_url,self.rome_search,format='text/html')
        self.assertEqual(response.status_code, 200)
    
    def test_search_wrong_date(self):
        response=self.client.post(self.index_url,self.wrong_date,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_search_many_guests(self):
        response=self.client.post(self.index_url,self.many_guests,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_search(self):
        response=self.client.post(self.index_url,self.fuzzer,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_search2(self):
        response=self.client.post(self.index_url,self.fuzzer_dest,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_all(self):
        response=self.client.post(self.index_url,self.fuzzer_all,format='text/html')
        self.assertEqual(response.status_code, 200)
##------------------------------------------##

##----------------About Page----------------##
class AboutPageTestCase(TestCase):
    def setUp(self):
        self.about_url=reverse('escapp:about')
        return super().setUp()

class AboutPageTest(AboutPageTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.about_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
##-----------------------------------------##

##----------------Account Page----------------##
class AccountPageTestCase(TestCase):
    def setUp(self):
        self.account_url=reverse('escapp:accountinfo')
        return super().setUp()

class AccountPageTest(AccountPageTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accountinfo.html')
##-----------------------------------------##

##----------------Account Page----------------##
class ContactPageTestCase(TestCase):
    def setUp(self):
        self.contact_url=reverse('escapp:contact')
        return super().setUp()

class ContactPageTest(ContactPageTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
##-----------------------------------------##

##----------------Account Info----------------##
class AccountInfoTestCase(TestCase):
    def setUp(self):
        self.accountinfo_url=reverse('escapp:accountinfo')
        return super().setUp()

class AccountInfoTest(AccountInfoTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.accountinfo_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accountinfo.html')
##-----------------------------------------##

##----------------Delete Account----------------##
class DeleteAccountTestCase(TestCase):
    def setUp(self):
        self.deleteaccount_url=reverse('escapp:deleteaccountcheck')
        return super().setUp()

class DeleteAccountTest(DeleteAccountTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.deleteaccount_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkdeleteaccount.html')
##-----------------------------------------##

##----------------Confirm Delete----------------##
class ConfirmDeleteTestCase(TestCase):
    def setUp(self):
        self.confirmdelete_url=reverse('escapp:confirmdelete')
        return super().setUp()

class ConfirmDeleteTest(ConfirmDeleteTestCase):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.confirmdelete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmdelete.html')
##-----------------------------------------##

##----------------Booking Form----------------##
class BookingFormTestCase(TestCase):
    def setUp(self):
        self.login_url=reverse('escapp:booklogin')
        self.booking_url=reverse('escapp:booking')
        self.login={
            'username': 'testerman',
            'password': 'testerman',
        }
        self.normal_booking={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'testerman@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.too_many_cardno={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'bob_tan@gmail.com',
            'request': 'NA',
            'card_no': '12341234123412342342342345324',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.too_many_cvv={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'bob_tan@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123456',
            'expiry': '0524',
        }
        self.fuzzer={
            'first_name': Fuzzer().randword(10),
            'last_name': Fuzzer().randword(3),
            'phone_number': Fuzzer().randnum(8),
            'email': Fuzzer('bob_tan@gmail.com').flipABit(),
            'request': Fuzzer().rand_punctuation(12),
            'card_no': Fuzzer().randnum(16),
            'billing': Fuzzer('8 somapah rd').flipABit(),
            'cvv': Fuzzer().randnum(3),
            'expiry': Fuzzer().randnum(4),
        }
        self.fuzzed_first_name={
            'first_name': Fuzzer('Testerman').flipABit(),
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'testerman@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.fuzzed_phone={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': Fuzzer().rand_punctuation(8),
            'email': 'testerman@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.fuzzed_email={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': Fuzzer('testerman@gmail.com').insertChar(),
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.fuzzed_card={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'testerman@gmail.com',
            'request': 'NA',
            'card_no': Fuzzer().rand_punctuation(16),
            'billing': '8 somapah rd',
            'cvv': '123',
            'expiry': '0524',
        }
        self.fuzzed_addr={
            'first_name': 'Testerman',
            'last_name': 'Test',
            'phone_number': '83245344',
            'email': 'testerman@gmail.com',
            'request': 'NA',
            'card_no': '1234123412341234',
            'billing': Fuzzer('8 somapah rd').insertChar(),
            'cvv': '123',
            'expiry': '0524',
        }
        return super().setUp()

class BookingFormTest(BookingFormTestCase):
    
    def test_can_view_page_correctly(self):
        response = self.client.get(self.booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking.html')

    def test_normal_booking(self):
        response=self.client.post(self.booking_url,self.normal_booking,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_too_many_cardno(self):
        response=self.client.post(self.booking_url,self.too_many_cardno,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_too_many_cvv(self):
        response=self.client.post(self.booking_url,self.too_many_cvv,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_booking(self):
        response=self.client.post(self.booking_url,self.fuzzer,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_firstname(self):
        response=self.client.post(self.booking_url,self.fuzzed_first_name,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_phone(self):
        response=self.client.post(self.booking_url,self.fuzzed_phone,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_email(self):
        response=self.client.post(self.booking_url,self.fuzzed_email,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_card(self):
        response=self.client.post(self.booking_url,self.fuzzed_card,format='text/html')
        self.assertEqual(response.status_code, 200)

    def test_fuzzer_addr(self):
        response=self.client.post(self.booking_url,self.fuzzed_addr,format='text/html')
        self.assertEqual(response.status_code, 200)

##----------------Booking Form----------------##


class Fuzzer:
    def __init__(self, valid_inpit=""):
        self.valid_input = valid_inpit
        self.characters = "!@#$%^&*()_+}{|:<>'?~`/"
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.numbers = "1234567890"

    def flipABit(self):
        randchar = randint(0, len(self.characters)-1)
        randpos = randint(0, len(self.valid_input)-1)

        return self.valid_input[:randpos] + self.characters[randchar] + self.valid_input[randpos+1:]

    def trim(self):
        randpos = randint(0, len(self.valid_input)-1)
        return self.valid_input[:randpos]

    def insertChar(self):
        randchar = randint(0, len(self.characters)-1)
        return self.valid_input + self.characters[randchar]

    def rand_punctuation(self, n=7):
        rand_punctuation = ""
        for i in range(n):
            randchar = randint(0, len(self.characters)-1)
            rand_punctuation += self.characters[randchar]
        return rand_punctuation

    def randword(self, n=7):
        randword = ""
        for i in range(n):
            randletter = randint(0, len(self.letters)-1)
            randword += self.letters[randletter]
        return randword

    def randnum(self, n=4):
        randnum = ""
        for i in range(n):
            rand = randint(0, len(self.numbers)-1)
            randnum += self.numbers[rand]
        return randnum

