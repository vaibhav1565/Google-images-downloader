import os
import sys
import time
from queue import Queue
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

def setup_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.accept_insecure_certs = True
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    return chrome_options

def setup_driver():
    try:
        service = Service(executable_path=os.path.join(os.getcwd(), 'chromedriver'))
        driver = webdriver.Chrome(service=service, options=setup_options())
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    except Exception as e:
        print(f"Error initializing Chrome driver: {e}")
        sys.exit(1)


def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load more content
        time.sleep(2.5)
        # Calculate the new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # Check if the page has finished loading (i.e., no more scroll)
        if new_height == last_height:
            break
        last_height = new_height  # Update last_height to the new value
    driver.execute_script("window.scrollTo(0,0);")


query = "Polar bear"
if sys.argv[1:]:
    query = sys.argv[1]


def scrape_images(url_queue: Queue,  show_text: bool = True):
    driver = setup_driver()
    driver.get(f'https://www.google.com/search?q={query}&udm=2')

    images_selector = "div[jscontroller='XW992c'] img[class='YQ4gaf']"
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, images_selector)))
    scroll_to_bottom(driver)

    images = driver.find_elements(By.CSS_SELECTOR, images_selector)
    selector = "img.sFlh5c.FyHeAf.iPVvYb"
    selector2 = "img.sFlh5c.FyHeAf"
    src = ''
    images_count = 1

    images[0].click()
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector)
        ))
        img = driver.find_element(By.CSS_SELECTOR, selector)
    except:
        img = driver.find_element(By.CSS_SELECTOR, selector2)
        print("--------------------Selector 2--------------------")

    src = img.get_attribute('src')
    url_queue.put((images_count, src))
    print(f"{images_count}. Scraped URL: {src}")

    images_count += 1
    l = len(images)
    while images_count <= l:
        try:
            images[images_count - 1].click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            ))
            img = driver.find_element(By.CSS_SELECTOR, selector)
        except:
            print("--------------------Selector 2--------------------")
            img = driver.find_elements(By.CSS_SELECTOR, selector2)[1]
            h1 = driver.find_element( By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div/div[2]/c-wiz/div/div[5]/div[1]/div/div[1]/a[1]/h1')
            print(h1.text)

        src = img.get_attribute('src')
        url_queue.put((images_count, src))
        print(f"{images_count}. Scraped URL: {src}")
        images_count += 1


if __name__ == '__main__':
    url_queue = Queue()
    scrape_images(url_queue, show_text = True)