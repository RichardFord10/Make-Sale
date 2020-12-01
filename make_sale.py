from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re
import pandas as pd
import sys
import csv
import os

# configure webdriver & headless chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options = chrome_options, executable_path=r'C:/Users/rford/Desktop/chromedriver/chromedriver.exe')

# current day format
currentDate = datetime.today().strftime('%Y-%m-%d')

#login function



item_number_list = [
'236804',
'236806',
'232795',
'235676',
'235677',
'236223',
'236221',
'236222',
'236634',
'232242',
'220815',
'234078',
'236088',
'236089',
'6209',
'236791',
'237155',
'237157',
'237334',
'4378',
'234665',
'236749',
'232748',
]






def login(user, pword = str):
    driver.get("https://#########.com/manager")
    Username = driver.find_element_by_id("bvuser")
    Password = driver.find_element_by_id("bvpass")
    Login = driver.find_element_by_xpath('//*[@id="form1"]/div/div[2]/input')
    Username.send_keys(user)
    Password.send_keys(pword)
    Login.click()
    print("Logging In...")
 
def save_sale():
    driver.find_element_by_xpath('//*[@id="editSaleForm"]/div/p/input').click()
    WebDriverWait(driver, 10)

def make_sale():
    driver.get("https://#########.com/manager/saleManager.php")
    select = Select(driver.find_element_by_xpath('//*[@id="saleTypeId"]'))
    #prompt for sale type
    prompt = "Choose Sale Type:\n\t1: Email Special\n\t2: Catalog Sale\n"
    while True:
        try:
            sale_type = int(input(prompt))
            if sale_type < 1 or sale_type > 2:
                raise ValueError
            break
        except ValueError:
            prompt = "Please enter 1 or 2:\n> "
    if sale_type == 1:
        select.select_by_value('1')
    else:
        select.select_by_value('2')
    #check 'Either' radio button on Currently Active
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form[1]/div/ul/li[2]/input[3]').click()
#check 'Either' radio button on Sold Online
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form[1]/div/ul/li[1]/input[3]').click()
#check 'Either' radio button on Sold to Customers
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form[1]/div/ul/li[3]/input[3]').click()
#check 'Either' radio button on Sales Taxable
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/form[1]/div/ul/li[4]/input[3]').click()

    WebDriverWait(driver, 1)
    driver.find_element_by_xpath('//*[@id="choosSaleTypeForm"]/div/ul/li[2]/input').click()
    WebDriverWait(driver, 3)

    #prompt for sale name
    sale_name = input("Enter Sale Name: ")
    WebDriverWait(driver, 1)
    driver.find_element_by_xpath('//*[@id="subject"]').send_keys(sale_name)


    #set expiration date
    expiration_date = input("Enter Expiration Date in format YEAR|MONTH|DAY")
    if re.match(r"[0-9]{4}-(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])", expiration_date):
        print("Input accepted")
    else:
        print("Bad input, please try again")
    driver.find_element_by_xpath('//*[@id="expireDateTime"]').send_keys(expiration_date)


    save_sale()

    #delete items showing from previous sale
    driver.find_element_by_xpath('//*[@id="regsearch"]/form[2]/div/ul/li[4]/input').click()

    save_sale()

    #choose from available inventory
    inv_avail = input('Inventory Available? Y/N  ')
    if inv_avail == 'Y':
        driver.find_element_by_xpath('//*[@name="isInStock"]').click()
        print('Selecting From Available Inventory...')
    else:
        pass

    WebDriverWait(driver, 10)


    for item_number in item_number_list:
        driver.find_element_by_xpath('//*[@id="name"]').clear()
        WebDriverWait(driver, 10)
        driver.find_element_by_xpath('//*[@id="name"]').send_keys(item_number)
        WebDriverWait(driver, 10)
        driver.find_element_by_xpath('//*[@id="searchinputs"]/div/div[2]/div[3]/input[3]').submit()
        WebDriverWait(driver, 10)
        add_to_list_id = 'addToList_{}'.format(item_number)
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
        add_to_list = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.ID, add_to_list_id)))
        add_to_list.click()
        WebDriverWait(driver, 5)
        print('Item {} has been added to Sale!'.format(item_number))
    print('Sale Creation Complete!')
    WebDriverWait(driver, 5)
    save_sale_id = 'saveItemList'
    save_sale_items = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.NAME, save_sale_id)))
    save_sale_items.click()
    WebDriverWait(driver, 10)
              





login(input("Enter Username: "), getpass("Enter Password: "))
make_sale()
WebDriverWait(driver, 10)
