from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time


options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
s = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(options = options, service=s)
driver.get('https://twitter.com/elonmusk/')

tweets_count = 10
tweets_txt = []
tweets_txt_for_output = []
number = 0
number_links = 0
links_to_comm = []
while number < tweets_count:

    if number > 0:
        driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(1)

        
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    tweets = soup.find_all('article', class_='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')

    for tweet in tweets:
        
        tmp = tweet
        tweet = tweet.find('div',class_= 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
        
        try:
            if tweet.text not in tweets_txt:
                tweets_txt.append(tweet.text)
                tweets_txt_for_output.append(tweet.text)
                number = number + 1

        except AttributeError:
            if tmp.text not in tweets_txt:
                tweets_txt.append(tmp.text)
                tweets_txt_for_output.append("***картинка или видео***")
                number = number + 1
                
        if number >= tweets_count:
            break

    elems = driver.find_elements(By.CSS_SELECTOR, ".css-1dbjc4n [href]")
    links = [elem.get_attribute('href') for elem in elems]
    for link in links:
        
        if str(link).find('/status/') != -1 and str(link).find('/photo/') == -1 and (link not in links_to_comm):
            links_to_comm.append(link)
            
            number_links+=1
        if number_links >= 10:
            break


users_links = []
for link in links_to_comm:
    driver.get(link)
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    comments = soup.find_all('div', class_='css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0')#('article', class_= 'css-1dbjc4n r-1loqt21 r-18u37iz r-1ut4w64 r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')
    #comments = soup.find_all('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs r-1ny4l3l')
    num = 0
    tmp = []

    for comment in comments:
        if comment.text != '@elonmusk':
            tmp.append('https://twitter.com/' + comment.text[1:])

            num = num + 1

    users_links.append(tmp)


print("\n\n   === Последние 10 твитов Илона Маска ===\n\n")
print("============================================")
for i in range(0,10):
    print(i+1, ' - ', tweets_txt_for_output[i])
    print("\n    Последние комменаторы:")
    print("   ", users_links[i][0], "\n   ", users_links[i][1],"\n   " ,users_links[i][2])
    print("============================================")
          

driver.quit()
