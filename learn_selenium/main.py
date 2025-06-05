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

driver.get('https://google.com')


WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
)

input_element = driver.find_element(By.CLASS_NAME,"gLFyf")
input_element.clear()
input_element.send_keys("Moses" + Keys.RETURN)

WebDriverWait(driver,5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Moses"))
)

link = driver.find_element(By.PARTIAL_LINK_TEXT,"Moses")
link.click()