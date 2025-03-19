import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Function to download resume from Google Drive
def download_resume(drive_id, save_path):
    url = f"https://drive.google.com/uc?export=download&id={drive_id}"
    session = requests.Session()
    response = session.get(url, stream=True)
    
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    
    print("✅ Resume downloaded successfully!")

# Hardcoded Credentials
NAUKRI_EMAIL = "manohar.shetty507@gmail.com"
NAUKRI_PASSWORD = "Manohar@1305"

# Resume details
GOOGLE_DRIVE_ID = "1hCJSrU_asQOi0lQKexoFMyeTXescVGqH"
RESUME_PATH = r"C:\Users\Manohar Shetty\Downloads\Manohar_Pinnamshetty.pdf"

# Step 1: Download the latest resume
download_resume(GOOGLE_DRIVE_ID, RESUME_PATH)

# Step 2: Launch Browser & Automate Login
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

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
    print("ℹ️ No popup found, continuing...")

# Click Login
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
login_button.click()

# Wait for Username Field
email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
driver.execute_script("arguments[0].scrollIntoView();", email_field)
email_field.click()
email_field.send_keys(NAUKRI_EMAIL)


# Enter Password
password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
password_field.send_keys(NAUKRI_PASSWORD)

# Click Login Button
login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
login_submit.click()

# Wait for login completion
time.sleep(5)
print("✅ Login successful!")

# Step 3: Navigate to Profile and Upload Resume
driver.get("https://www.naukri.com/mnjuser/profile")

# Wait for Resume Upload Section
upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

# Upload Resume
upload_btn.send_keys(RESUME_PATH)

# Wait for upload to complete
time.sleep(10)

print("✅ Resume uploaded successfully!")

# Close browser
driver.quit()
