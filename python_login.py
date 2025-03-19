import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configurations
NAUKRI_EMAIL = "manohar.shetty507@gmail.com"
NAUKRI_PASSWORD = "Manohar@1305"

# Launch Browser
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

# Open Naukri
driver.get("https://www.naukri.com/")

# Handle popups (if any)
try:
    popup_close = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Later')]")))
    popup_close.click()
except:
    print("No popup found, continuing...")

# Click Login
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
login_button.click()

# Debug: Print page source
time.sleep(2)
print(driver.page_source)  # Check if login form is visible

# Wait for Username Field (Using XPATH instead of ID)
email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
email_field.send_keys(NAUKRI_EMAIL)

# Enter Password
password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
password_field.send_keys(NAUKRI_PASSWORD)

# Click Login Button
login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
login_submit.click()

# Wait for login completion
time.sleep(5)

print("Login successful!")
driver.quit()