
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


def BLAST(query):
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi')

    driver.find_element_by_id('homeBlastn').click()
    driver.find_element_by_id('seq').send_keys(query)
    driver.find_element_by_id('blastButton1').click()

    wait = WebDriverWait(driver, 30)
    download = wait.until(expected_conditions.visibility_of_element_located((By.ID, 'btnDwnld')))
    download.click()
