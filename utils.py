import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


def get_firefox_driver(profile_path):
    service  = Service(executable_path=GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.add_argument('-profile')
    options.add_argument(profile_path)
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def sort_office_by_zipnum(driver, zipnum):
    search_box = driver.find_element(By.XPATH, '//*[@id="search-input"]')
    search_box.send_keys(zipnum)
    search_box.send_keys(Keys.ENTER)


def get_office_btn(driver, num):
    office = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/main/form/div[2]/div[4]/div/div/div[{}]'.format(num))
    return office


def get_month(driver):
    return driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/form/div[2]/div[2]/div[1]/div/div/div/div/div/div/span[1]').text


def get_office_name(driver):
    return driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[3]/div/div').text


def start_permit_appt(driver):
    driver.get('https://skiptheline.ncdot.gov')
    driver.implicitly_wait(3)
    btn_appt = driver.find_element(By.XPATH, '//*[@id="cmdMakeAppt"]').click()
    permit = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/main/form/div[2]/div[1]/div[1]/div/div[10]').click()
    time.sleep(1)


def start_license_appt(driver):
    driver.get('https://skiptheline.ncdot.gov')
    driver.implicitly_wait(3)
    btn_appt = driver.find_element(By.XPATH, '//*[@id="cmdMakeAppt"]').click()
    license = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/main/form/div[2]/div[1]/div[1]/div/div[1]').click()
    time.sleep(1)


def make_appt(driver, config):
    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/form/div[2]/div[3]/div/div[1]/div[2]')
    next_btn.click()
    time.sleep(4)

    # Fill in the form
    first_name = driver.find_element(By.XPATH, '//*[@id="StepControls_0__Model_Value_Properties_0__Value"]')
    first_name.send_keys(config['first name'])
    last_name = driver.find_element(By.XPATH, '//*[@id="StepControls_0__Model_Value_Properties_1__Value"]')
    last_name.send_keys(config['last name'])
    time.sleep(1)
    phone = driver.find_element(By.XPATH, '//*[@id="StepControls_0__Model_Value_Properties_2__Value"]')
    phone.send_keys(config['phone number'])
    email = driver.find_element(By.XPATH, '//*[@id="StepControls_0__Model_Value_Properties_3__Value"]')
    email.send_keys(config['email'])
    email = driver.find_element(By.XPATH, '//*[@id="StepControls_0__Model_Value_Properties_4__Value"]')
    email.send_keys(config['email'])
    time.sleep(1.2)
    recaptcha = driver.find_element(By.XPATH, '//div[@class=\'g-recaptcha\']')
    recaptcha.click()
    next_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/main/form/div[2]/div[3]/div/div[1]/div[2]/input')
    next_btn.click()
    time.sleep(2)

    # Final confirmation!
    final = driver.find_element(By.XPATH, '/html/body/div/div/div/main/form/div[3]/div[2]')
    final.click()
