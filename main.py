import requests
import os
from dotenv import load_dotenv
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# TODO Maybe run ngrok here?
# Webdriver: https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/
# chromedrvier.exe should be in current directory

print("Attempting to get ngrok url...")
response = requests.get("http://localhost:4040/api/tunnels")
if response.status_code != 200:
    print("No response from ngrok on port 4040, aborting...")
    exit()

response = response.json()["tunnels"][0]["public_url"]
# cutting http[s]://
url = response.split("/")[-1]
print(f"ngrok url: {url}")

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_FOLDER = os.environ.get("ADMIN_FOLDER")

print("Getting current domain from database...")
mydb = mysql.connector.connect(
  host="localhost",
  user=DB_USER,
  password=DB_PASS,
  database=DB_NAME
)

mycursor = mydb.cursor()
sql = "SELECT domain FROM ps_shop_url"

print(sql)

mycursor.execute(sql)
# first value of tuple
old_url = mycursor.fetchone()[0]

print(f"Current domain: {old_url}")
print("Updating domains in database...")

sql = (f"UPDATE ps_shop_url SET domain = '{url}', domain_ssl = '{url}'"
      f" WHERE domain = '{old_url}' AND domain_ssl = '{old_url}'")

print(sql)
mycursor.execute(sql)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")

admin_url = f"http://{url}/{ADMIN_FOLDER}"
print(f"Starting webdriver at {admin_url}")

driver = webdriver.Chrome("chromedriver.exe")
driver.maximize_window()
driver.get(admin_url)
print(driver.title)
login = driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "passwd")
login.send_keys(ADMIN_USER)
password.send_keys(ADMIN_PASSWORD)
login.send_keys(Keys.RETURN)

driver.implicitly_wait(5)
preferences_button = driver.find_element(By.ID, "subtab-ShopParameters")
preferences_button.click()
driver.implicitly_wait(3)
traffic_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Ruch") # Traffic in ENG
traffic_button.click()

driver.implicitly_wait(5)
domain_box = driver.find_element(By.ID, "meta_settings_shop_urls_form_domain")
domain_box.send_keys(Keys.RETURN)

print("Closing, DONE!")
driver.close()