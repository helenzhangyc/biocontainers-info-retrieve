from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import csv

# Get the names of all deployed biocontainers and stored all of their names into app_name
biocontainer_url = "https://www.rcac.purdue.edu/knowledge/biocontainers"
page = urlopen(biocontainer_url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


applications = soup.find_all("li", attrs={'class', 'toctree-l1'})

app_name = []
for item in applications:
    app_name.append(item.text)


# For each name, go to biocontainers.pro/tools/{name} to get the number of downloads
downloads = []
for name in app_name:
    url = f"https://biocontainers.pro/tools/{name}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.get(url)
    content = driver.find_element(By.CLASS_NAME, "property-content")
    downloads.append(content.text)


# write to a csv file
dict = {'Application Name': app_name, "Number of Downloads": downloads}
df = pd.DataFrame(dict)
df.to_csv('biocontainer_info.csv')



