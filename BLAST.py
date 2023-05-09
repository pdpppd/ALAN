
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def BLAST(query):
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi')

    driver.find_element_by_id('homeBlastn').click()
    driver.find_element_by_id('seq').send_keys(query)
    driver.find_element_by_id('blastButton1').click()
