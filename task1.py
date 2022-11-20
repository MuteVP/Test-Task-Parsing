from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
ua = UserAgent()
userAgent = ua.random

print(" Start...\n")
options.add_argument(f'user-agent={userAgent}')
s = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(options=options, service=s)
driver.delete_all_cookies()     #в данной задаче лучшего решения для обхода защиты нет;
# любая подмена cookie сопряжена с возникающими ошибками;
# сохранять же куки нет никакой необходимости;
# данный способ удаляет все куки в текущей сессии и выполняет поставленную задачу

driver.get('https://www.nseindia.com/')

menu_marketData = driver.find_element(By.CSS_SELECTOR, "#link_2")
time.sleep(0.1)
hover = ActionChains(driver).move_to_element(menu_marketData)
hover.perform()

menu_marketData_preOpenMarket = driver.find_element(By.CSS_SELECTOR,
                                                    "a[href='/market-data/pre-open-market-cm-and-emerge-market']")
time.sleep(0.1)
driver.delete_all_cookies()
menu_marketData_preOpenMarket.click()
time.sleep(3)
final_prices = driver.find_elements(By.CSS_SELECTOR, "td[class='bold text-right']")
prices = [final_price.get_attribute("innerHTML") for final_price in final_prices]

names_tags = driver.find_elements(By.CSS_SELECTOR, "td a[target='_blank']")
names = [name.get_attribute("innerHTML") for name in names_tags]

for i in range(0, len(names)):
    if names[i].find(';') != -1:
        names[i] = names[i][:names[i].find(';')] + names[i][names[i].find(';') + 1:]

file = open('prices.csv', 'w')
for i in range(0, len(prices)):
    file.write(names[i] + ";" + prices[i] + "\n")

file.close()

# ===пользовательский сценарий===

driver.delete_all_cookies()
driver.find_element(By.CSS_SELECTOR, "img[title='NSE India, National Stock Exchange']").click()
time.sleep(3)
graph = driver.find_element(By.CSS_SELECTOR, "div[role='tablist']")
graph.location_once_scrolled_into_view

time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "a[id='tabList_NIFTYBANK']").click()
time.sleep(3)
driver.execute_script("window.scrollBy(0, 100);")
time.sleep(2)
driver.delete_all_cookies()
# driver.find_element(By.XPATH,"//*[@id='tab4_gainers_loosers']/div[3]/a").click()
driver.find_element(By.CSS_SELECTOR, "a[href='/market-data/live-equity-market?symbol=NIFTY BANK']").click()

time.sleep(3)

driver.delete_all_cookies()
driver.find_element(By.CSS_SELECTOR, "option[value='NIFTY ALPHA 50']").click()

time.sleep(10)

try:
    table = driver.find_element(By.CSS_SELECTOR, "table[id='equityStockTable']").send_keys(Keys.END)

except:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(3)
print(" End.\n Results locate in prices.csv")
driver.quit()
