from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
service = Service(executable_path='./chromedriver')
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get('https://orteil.dashnet.org/cookieclicker/')

WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH,"//div[text()='English']"))
)
language = driver.find_element(By.XPATH,"//div[text()='English']")
language.click()

WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,"bigCookie"))
)
cookie = driver.find_element(By.ID,"bigCookie")
cookie_count = driver.find_element(By.ID,"cookies")
while True:
    cookie.click()
    for _ in range(19,-1,-1):
        price_element = driver.find_element(By.ID, "productPrice"+str(_))
        if price_element.text:
            price = int(price_element.text.replace(',',''))
            if int(cookie_count.text.split()[0].replace(',','')) >= price:
                driver.execute_script("arguments[0].click();", price_element)