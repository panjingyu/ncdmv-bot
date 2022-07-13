import argparse
import time
import calendar
import yaml

from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

from utils import *


def main(driver, config):
    start_permit_appt(driver)
    success = False
    cnt = 0
    while not success:
        if cnt >= 5:
            cnt = 0
            time.sleep(10 * 60)
            now = datetime.now().strftime('%m/%d-%H:%M:%S')
            print(f'[{now}] Refreshed page')
            start_permit_appt(driver)
        cnt = cnt + 1
        check_order = range(1, 6)
        month_list = list(calendar.month_name)
        for i in check_order:
            sort_office_by_zipnum(driver, '27705')
            time.sleep(3)
            btn_office = get_office_btn(driver, i).click()
            time.sleep(3)
            month, office = get_month(driver), get_office_name(driver)
            time.sleep(3)
            now = datetime.now().strftime('%m/%d-%H:%M:%S')
            if month_list.index(month) > 7:
                print(f'[{now}] Skipped {month} in {office}')
                back_btn = driver.find_element(By.XPATH, '//*[@id="BackButton"]')
                back_btn.click()
            else:
                # get earliest date
                earliest_day = driver.find_element(By.CLASS_NAME, 'ui-datepicker-current-day')
                if int(earliest_day.text) < 10:
                    # Should send alarm to me
                    print(f'[{now}] Found {month} {earliest_day.text} in {office}!')
                    make_appt(driver, config)
                    success = True
                    break
                else:
                    print(f'[{now}] Skipped {month} {earliest_day.text} in {office}')
                    back_btn = driver.find_element(By.XPATH, '//*[@id="BackButton"]')
                    back_btn.click()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default='config.yaml',
                        help='Config yaml file.')
    args = parser.parse_args()
    driver = get_firefox_driver()
    config = yaml.safe_load(open(args.config, 'r'))
    while True:
        try:
            # restart automatically when exception occurs
            main(driver, config)
            break
        except StaleElementReferenceException as e:
            print(e)
        except ElementClickInterceptedException as e:
            print(e)
        except NoSuchElementException as e:
            print(e)
