from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

driver.get("https://www.google.com/search?client=firefox-b-d&q=tech+with+tim")

element = driver.find_element(By.PARTIAL_LINK_TEXT, "Tech With Tim")
print(dir(element))
print(element.text)
print(element.tag_name)
print(element.size)
print(element.parent)
