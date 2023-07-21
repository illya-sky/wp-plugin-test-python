from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import ImageGrab
from faker import Faker
import os
from Forms import login

faker = Faker()

fkr_day_of_month = faker.day_of_month()
# there is no October
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "November", "December"]
fkr_month = faker.word(ext_word_list=months)
# there is an error that the year should be from 1900, but indeed it takes values from 1970 only
fkr_year = faker.random_int(1900, 2017)
fkr_first_name = faker.first_name()
fkr_name = fkr_first_name+' '+faker.last_name()
fkr_nickname = str.lower(fkr_first_name)+str(faker.random_int(1, 1000))
fkr_email = faker.email()
fkr_address = faker.address().replace('\n', ' ')
fkr_url = faker.url()

username = login.WP_USERNAME
password = login.WP_PASSWORD
url = 'http://qa-test.nova-green.ru/wp-admin/options-general.php?page=qa-test-settings'


@pytest.mark.parametrize('i, name, nickname, address, day, month, year, email, website',
                         [
                             ('Test 1 Positive', fkr_name, fkr_nickname, fkr_address, fkr_day_of_month, fkr_month, fkr_year, fkr_email, fkr_url),  # positive
                             ('Test 2 Negative', ' ', ' ', '!@1', '43', 'December', '2050', 'email address', 'hello.com'),  # negative
                             ('Test 3 Negative', '1', '', '', '0', 'January', '-10', '', ' '),  # negative
                         ])
def test_forms(i, name, nickname, address, day, month, year, email, website):

    # login variables
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(url)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'user_login')))

    user_login = driver.find_element(By.ID, 'user_login')
    user_pass = driver.find_element(By.ID, 'user_pass')
    rememberme = driver.find_element(By.ID, 'rememberme')
    wplogin = driver.find_element(By.ID, 'wp-submit')

    # login to admin

    user_login.send_keys(username)
    user_pass.send_keys(password)
    rememberme.click()
    wplogin.click()

    assert driver.current_url == url, 'Log in failed'

    # form variables
    qa_test_fullname = driver.find_element(By.ID, 'qa_test_fullname')
    qa_test_nickname = driver.find_element(By.ID, 'qa_test_nickname')
    qa_test_address = driver.find_element(By.ID, 'qa_test_address')
    select = Select(driver.find_element(By.ID, 'qa_test_dob_m'))
    qa_test_dob_y = driver.find_element(By.ID, 'qa_test_dob_y')
    qa_test_email = driver.find_element(By.ID, 'qa_test_email')
    qa_test_web = driver.find_element(By.ID, 'qa_test_web')

    # data input
    qa_test_fullname.clear()
    qa_test_fullname.send_keys(str(name))

    qa_test_nickname.clear()
    qa_test_nickname.send_keys(str(nickname))

    qa_test_address.clear()
    qa_test_address.send_keys(address)

    qa_test_dob_d = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'qa_test_dob_d')))
    qa_test_dob_d.clear()
    qa_test_dob_d.send_keys(str(day))

    select.select_by_visible_text(str(month))

    qa_test_dob_y.clear()
    qa_test_dob_y.send_keys(str(year))

    qa_test_email.clear()
    qa_test_email.send_keys(email)

    qa_test_web.clear()
    qa_test_web.send_keys(str(website))

    qa_test_web = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.NAME, 'Submit')))
    qa_test_web.click()

    time.sleep(3)

    try:
        driver.find_element(By.XPATH, '//div[@id="setting-error-settings_updated"]//child::strong')
        print(' ____ ' + i + ' PASSED')
    except NoSuchElementException:
        snapshot = ImageGrab.grab()
        save_path = os.path.abspath(os.getcwd())+'\\Failed tests\\' + i + '.jpg'
        snapshot.save(save_path)
        snapshot.show()
        print(' _!__ ' + i + ' FAILED')
