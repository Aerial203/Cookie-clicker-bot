from selenium import webdriver
import time

chrome_driver_path = "C:\Development\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

cookies_endpoint = "http://orteil.dashnet.org/experiments/cookie/"

driver.get(url=cookies_endpoint)


def current_balance():
    cookie_money = driver.find_element_by_id("money")
    money = int(cookie_money.text.replace(",", ""))
    return money


def get_cookie_price():
    all_cookie_prices = []
    all_cookie_prices_tag = driver.find_elements_by_css_selector("#store b")
    for price in all_cookie_prices_tag:
        try:
            p = int(price.text.split(" - ")[1].replace(",", ""))
        except IndexError:
            pass
        else:
            all_cookie_prices.append(p)
    return all_cookie_prices


cookie_button = driver.find_element_by_id("cookie")
all_store = driver.find_elements_by_css_selector("#store div")
store_attributes = [item.get_attribute("id") for item in all_store]

timeout = time.time() + 5   # 5 sec from now
timeout_five_minute = time.time() + 60*5   # 5 minutes from now
current_amount: int
while True:
    cookie_button.click()
    if time.time() > timeout:
        current_amount = current_balance()
        cookie_price = get_cookie_price()
        p = None
        for price in cookie_price:
            if current_amount >= price:
                p = price
        try:
            highest_price_index = cookie_price.index(p)
            buy_store = store_attributes[highest_price_index]
            store = driver.find_element_by_id(buy_store)
            store.click()
        except ValueError:
            pass
        timeout = time.time() + 5

    if time.time() > timeout_five_minute:
        print(current_balance())
        driver.close()
        break

