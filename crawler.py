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


def scroll_to_bottom(driver, check_interval=0.5, max_time=60):
    start_time = time.time()

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(check_interval)

        try:
            footer = driver.find_element(By.CSS_SELECTOR, "span.B4GxFc")
            if footer.is_displayed():
                break
        except:
            pass  # Footer not found yet

        if time.time() - start_time > max_time:
            print("Reached max scroll time without finding footer.")
            break

    driver.execute_script("window.scrollTo(0, 0);")
    print(f"Total time taken for scrolling- {(time.time() - start_time):.2f} seconds")


def scrape_images(image_url_queue: Queue, query: str, print_urls: bool = True):
    driver = setup_driver()
    driver.get(f'https://www.google.com/search?q={query}&udm=2')

    images_selector = "div[jscontroller='XW992c'] img[class='YQ4gaf']"
    WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.CSS_SELECTOR, images_selector)))
    scroll_to_bottom(driver)

    images = driver.find_elements(By.CSS_SELECTOR, images_selector)
    primary_selector = "img.sFlh5c.FyHeAf.iPVvYb"
    fallback_selector = "img.sFlh5c.FyHeAf"
    image_url = ''
    image_index = 1

    images[0].click()
    is_fallback = False
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, primary_selector)
        ))
        image_element = driver.find_element(By.CSS_SELECTOR, primary_selector)
    except:
        image_element = driver.find_element(By.CSS_SELECTOR, fallback_selector)
        is_fallback = True
        print("#########################################################")

    image_url = image_element.get_attribute('src')
    image_url_queue.put((image_index, image_url))
    if print_urls:
        print(f"{image_index}. {image_url}")

    if is_fallback:
        print("#########################################################")

    image_index += 1
    total_images = len(images)
    while image_index <= total_images:
        is_fallback = False
        try:
            images[image_index - 1].click()

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, primary_selector)
            ))
            image_element = driver.find_element(
                By.CSS_SELECTOR, primary_selector)
            # image_element = driver.find_element(
            #     By.CSS_SELECTOR, fallback_selector)
            
            # ie = driver.find_elements(
            #     By.CSS_SELECTOR, fallback_selector)
            # for e in ie:
            #     print(e.get_attribute("src"))
        except:
            print("#########################################################")
            # is_fallback = True

            image_elements = driver.find_elements(
                By.CSS_SELECTOR, fallback_selector)
            image_element = image_elements[1]
            # for e in image_elements:
            #     print(e.get_attribute("src"))
            # image_title = image_element.get_attribute("alt")
            # print(f"Image title- {image_title}")

            pass

        image_url = image_element.get_attribute('src')
        if is_fallback:
            print("image url", image_url)
            if not image_url.startswith("https://encrypted-tbn0.gstatic.com/"):
                try:
                    ie = driver.find_element(
                        By.CSS_SELECTOR, primary_selector)
                    print("ie")
                except:
                    print('ei')
                    pass
        image_url_queue.put((image_index, image_url))
        if print_urls:
            print(f"{image_index}. {image_url}")
        image_index += 1

        if is_fallback:
            print("#########################################################")

if __name__ == '__main__':
    query = sys.argv[1]

    image_url_queue = Queue()
    scrape_images(image_url_queue, query)