from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys 
import time


options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
ua = UserAgent()
userAgent = ua.random
#print(f'user-agent={userAgent}')
print(" Start...\n")
options.add_argument(f'user-agent={userAgent}')
s = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(options = options, service=s)
driver.delete_all_cookies()
driver.get('https://www.nseindia.com/')

menu_marketData = driver.find_element(By.XPATH,"//a[@id='link_2']")
time.sleep(0.1)
hover = ActionChains(driver).move_to_element(menu_marketData)
hover.perform()
menu_marketData_preOpenMarket = driver.find_element(By.XPATH,"//a[@href='/market-data/pre-open-market-cm-and-emerge-market']")
time.sleep(0.1)
driver.delete_all_cookies()
menu_marketData_preOpenMarket.click()
time.sleep(3)
final_prices = driver.find_elements(By.XPATH, "//td[@class='bold text-right']")
prices = [final_price.get_attribute("innerHTML") for final_price in final_prices]

names_tags = driver.find_elements(By.XPATH, "//td/a[@target='_blank']")
names = [name.get_attribute("innerHTML") for name in names_tags]

for i in range(0,len(names)):
    if names[i].find(';') != -1:
        names[i] = names[i][:names[i].find(';')] + names[i][names[i].find(';')+1:]

file = open('prices.csv', 'w')
for i in range(0,len(prices)):
    file.write(names[i]+";"+prices[i]+"\n")
 
file.close()

#===пользовательский сценарий===

driver.delete_all_cookies()
driver.find_element(By.XPATH,"//img[@title='NSE India, National Stock Exchange']").click()
time.sleep(3)
graph = driver.find_element(By.XPATH, "//div[@role='tablist']")
graph.location_once_scrolled_into_view
#driver.execute_script("window.scrollBy(0, 400);")
time.sleep(3)
driver.find_element(By.XPATH,"//a[@id='tabList_NIFTYBANK']").click()
time.sleep(3)
'''view_all = '''
driver.execute_script("window.scrollBy(0, 100);")
time.sleep(2)
driver.delete_all_cookies()
driver.find_element(By.XPATH,"//*[@id='tab4_gainers_loosers']/div[3]/a").click()
#"//div[@class='tab-content']/div/a").click()
#print(view_all.get_attribute("innerHTML"))
#ActionChains(driver).move_to_element(view_all).click(view_all).perform()
time.sleep(3)
#driver.find_element(By.XPATH,"//select[@id='equitieStockSelect']").click()
#time.sleep(3)
#NiftyAlpha =
driver.delete_all_cookies()
driver.find_element(By.XPATH,"//option[@value='NIFTY ALPHA 50']").click()
#driver.move_to_element()
time.sleep(10)

try:
    table = driver.find_element(By.XPATH,"//table[@id='equityStockTable']").send_keys(Keys.END)

except:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    

time.sleep(3)
print(" End.\n Results locate in prices.csv")
driver.quit()
