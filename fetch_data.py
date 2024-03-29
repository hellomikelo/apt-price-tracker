from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import json
import selenium


def get_data():
    # Initialize Chrome Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(options=options) 
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options) 
    driver.implicitly_wait(90)
    # driver.set_page_load_timeout(90)

    # Load the URL and get the page source
    URL = 'https://liveat678bellflower.com/floor-plans.aspx'
    driver.get(URL)

    results_container = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'par_10617247'))
    )

    assert type(results_container) == selenium.webdriver.remote.webelement.WebElement, "results_container is a wrong type! Please check."

    sections = results_container.find_elements(By.CLASS_NAME, "unit-container")

    assert len(sections) != 0, "No sections found! Please check."

    # Find elements
    res = []
    for section in sections:
        unit_type_str = section.find_element(By.XPATH, '//*[@id="text-area"]/div/div[1]/h2').get_attribute("innerHTML").strip()
        unit_price_str = section.find_element(By.CLASS_NAME, "unit-rent").get_attribute("innerHTML")
        unit_number_str = section.find_element(By.CLASS_NAME, "unit-number").get_attribute("innerHTML")
        unit_sqft_str = section.find_element(By.CLASS_NAME, "unit-sqft").get_attribute("innerHTML")
        available_date_str = section.find_element(By.CSS_SELECTOR, "div.unit-container-left > div:nth-child(3)").get_attribute("innerHTML")
        lease_term_str = section.find_element(By.CSS_SELECTOR, "div.unit-container-left > div:nth-child(4)").get_attribute("innerHTML")

        unit_sqft = int(re.findall(r'\d+', unit_sqft_str.replace(',', ''))[0])
        unit_number = int(re.findall(r'\d+', unit_number_str)[0])
        unit_price = unit_price_str.replace('$', '').replace(',', '').strip()
        unit_price = int(unit_price[-4:])
        available_date = re.findall(r'(\d{2}/\d{2}/\d{4}|NOW)', available_date_str)[0]
        lease_term = int(lease_term_str.replace('Lease Term: ', '').strip())
        
        assert unit_type_str == 'The Preserve', 'Wrong unit type! Please check.'
        
        _res = {"unit_number": unit_number,
                "unit_price": unit_price,
                "available_date": available_date,
                "lease_term": lease_term,
                "unit_sqft": unit_sqft
                }
        
        res.append(_res)

    res2 = sorted(res, key=lambda x: (x['unit_price'], x['unit_number']))

    [print(_res) for _res in res2]

    # Write out results
    with open("latest_prices.json", "w") as f:
        # Dump the list to the file
        json.dump(res2, f)

if __name__ == '__main__':
    get_data()