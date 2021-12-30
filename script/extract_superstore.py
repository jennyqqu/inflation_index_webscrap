from selenium import webdriver
import selenium as selenium
from selenium.webdriver.common.by import By

import time
import pandas as pd

import numpy as np


# helper function

def click_load_more(driver, n):
    last_button = False
    i = 0
    while not last_button and i < n:
        print('here')
        try:
            element_load_more_button = driver.find_element_by_class_name('primary-button--load-more-button')
            time.sleep(5)
            webdriver.ActionChains(driver).move_to_element(element_load_more_button).click(
                element_load_more_button).perform()
            print(i)
            print('click')
            i += 1
            # element_load_more_button.click()
            # time.sleep(3)
        except selenium.common.exceptions.NoSuchElementException:
            last_button = True
            print('stop')
            print(1)
    return driver


def extract_item_details_superstore(driver, item_id):
    # find product brand if exist
    try:
        element_brand = driver.find_element(by=By.CSS_SELECTOR,
                                            value='#site-content > div > div > div > div.product-grid > div.product-grid__results \
                                           > div.product-grid__results__products > div > ul > li:nth-child(' + str(
                                                item_id) + ') > div > div > \
                                            div.product-tile__details > div.product-tile__details__info > h3 > a > span > span.product-name__item.product-name__item--brand')

        brand_text = element_brand.get_attribute('innerHTML')
    except selenium.common.exceptions.NoSuchElementException:
        brand_text = np.NaN

    # find product name
    try:
        element_name = driver.find_element(by=By.CSS_SELECTOR,
                                           value='#site-content > div > div > div > div.product-grid > div.product-grid__results \
                                           > div.product-grid__results__products > div > ul > li:nth-child(' + str(
                                               item_id) + ') > div > div > \
                                            div.product-tile__details > div.product-tile__details__info > h3 > a > span > span.product-name__item.product-name__item--name')

        name_text = element_name.get_attribute('innerHTML')
    except selenium.common.exceptions.NoSuchElementException:
        name_text = np.NaN

    # print(name_text)

    # find product price
    try:
        element_price = driver.find_element(by=By.CSS_SELECTOR,
                                            value='#site-content > div > div > div > div.product-grid \
                                             > div.product-grid__results > div.product-grid__results__products \
                                              > div > ul > li:nth-child(' + str(item_id) + ') > div > div > div.product-tile__details \
                                              > div.product-tile__details__info > div > div.product-prices.product-prices--product-tile \
                                              > div > div > span > span.price__value.selling-price-list__item__price.selling-price-list__item__price--now-price__value')

        price_text = element_price.get_attribute('innerHTML')

    except selenium.common.exceptions.NoSuchElementException:
        price_text = np.NaN

    # print(price_text)

    # find product unit price
    try:
        element_unit_price = driver.find_element(by=By.CSS_SELECTOR,
                                                 value='#site-content > div > div > div > div.product-grid > \
                                           div.product-grid__results > div.product-grid__results__products > div > ul > \
                                           li:nth-child(' + str(item_id) + ') > div > div > div.product-tile__details > \
                                            div.product-tile__details__info > div > div.product-prices.product-prices--product-tile \
                                            > ul > li > span > span.price__value.comparison-price-list__item__price__value')

        unit_price_text = element_unit_price.get_attribute('innerHTML')


    except selenium.common.exceptions.NoSuchElementException:
        unit_price_text = np.NaN
        print(1)

    # find product unit vol
    try:
        element_unit_volume = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='#site-content > div > div > div > div.product-grid > div.product-grid__results \
                                                       > div.product-grid__results__products > div > ul > li:nth-child(' + str(
                                                      item_id) + ') > div \
                                                       > div > div.product-tile__details > div.product-tile__details__info > div \
                                                       > div.product-prices.product-prices--product-tile > ul > li:nth-child(1) \
                                                       > span > span.price__unit.comparison-price-list__item__price__unit')
        unit_volume_text = element_unit_volume.get_attribute('innerHTML')


    except selenium.common.exceptions.NoSuchElementException:
        unit_volume_text = np.NaN
        print(1)

    return driver, brand_text, name_text, price_text, unit_price_text, unit_volume_text


def create_item_info_table(driver, item_category):
    item_info = pd.DataFrame.from_dict({
        'item_category': [],
        'item_index': [],
        'item_brand': [],
        'item_name': [],
        'item_price': [],
        'item_unit_price': [],
        'item_unit_volume': []
    })

    # item_info
    item_index = []
    item_brand = []
    item_name = []
    item_price = []
    item_unit_price = []
    item_unit_volume = []

    for n, l in enumerate(item_list):
        print(l)
        print(n)
        item_id = n + 1

        driver, brand_text, name_text, price_text, unit_price_text, unit_volume_text = extract_item_details_superstore(
            driver, item_id)
        item_index.append(str(item_id))
        item_brand.append(brand_text)
        item_name.append(name_text)
        item_price.append(price_text)
        item_unit_price.append(unit_price_text)
        item_unit_volume.append(unit_volume_text)

    print(item_category)
    # add those columns in to the item_info

    item_info['item_index'] = item_index
    item_info['item_brand'] = item_brand
    item_info['item_name'] = item_name
    item_info['item_price'] = item_price
    item_info['item_unit_price'] = item_unit_price
    item_info['item_unit_volume'] = item_unit_volume
    item_info['item_category'] = item_category

    return (driver, item_info)


# open webdriver
driver = webdriver.Chrome('/Users/qianqu/Code/project/inflation_index_webscape/webdriver/chromedriver')

# create csv to hold the keywords and load it in
grocery_list = pd.read_csv('/Users/qianqu/Code/project/inflation_index_webscape/data/grocery_category.csv')

all_item_info = pd.DataFrame.from_dict({
    'item_category': [],
    'item_index': [],
    'item_brand': [],
    'item_name': [],
    'item_price': [],
    'item_unit_price': [],
    'item_unit_volume': []
})

for item_category in grocery_list['grocery_category']:
    print(item_category)

    # item_category = 'potato'

    driver.get("https://www.realcanadiansuperstore.ca/search?search-bar=" + item_category)
    # example: tomato
    time.sleep(10)

    driver = click_load_more(driver, 2)

    print('step 3')
    item_list = driver.find_elements(by='xpath',
                                     value='//*[@id="site-content"]/div/div/div/div[2]/div[2]/div[3]/div/ul/li')

    print('step 4')
    driver, item_info = create_item_info_table(driver, item_category)

    all_item_info = all_item_info.append(item_info)
