import os
import logging
import time
import boto3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# AWS S3 Configurations
BUCKET_NAME = "profile1305"
S3_OBJECT_KEY = "Manohar_Pinnamshetty.pdf"
DOWNLOAD_PATH = os.path.expanduser("~/Downloads/resume.pdf")

# Naukri Credentials
EMAIL = "manohar.shetty507@gmail.com"
PASSWORD = "Manohar@1305"


def download_resume_from_s3():
    """Download the latest resume from S3."""
    logger.info("Connecting to AWS S3...")
    s3 = boto3.client("s3")

    try:
        s3.download_file(BUCKET_NAME, S3_OBJECT_KEY, DOWNLOAD_PATH)
        logger.info(f"✅ Resume downloaded successfully: {DOWNLOAD_PATH}")
    except Exception as e:
        logger.error(f"❌ Error downloading resume: {e}")
        return False
    return True


def upload_resume_naukri():
    """Automate Naukri.com resume upload."""
    logger.info("Launching browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        logger.info("Opening Naukri.com...")
        driver.get("https://www.naukri.com/")

        # Handle popups (if any)
        try:
            popup_close = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Later')]")))
            popup_close.click()
            logger.info("Closed popup.")
        except:
            logger.info("ℹ️ No popup found, continuing...")

        # Click Login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
        login_button.click()
        logger.info("Clicked Login...")

        # Wait for Username Field
        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']")))
        driver.execute_script("arguments[0].scrollIntoView();", email_field)
        email_field.click()
        email_field.send_keys(EMAIL)
        logger.info("Entered Email...")

        # Enter Password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_field.send_keys(PASSWORD)

        # Click Login Button
        login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
        login_submit.click()

        # Wait for login completion
        time.sleep(5)
        logger.info("✅ Login successful!")

        # Step 3: Navigate to Profile and Upload Resume
        driver.get("https://www.naukri.com/mnjuser/profile")

        # Wait for Resume Upload Section
        upload_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))

        # Upload Resume
        upload_btn.send_keys(DOWNLOAD_PATH)

        # Wait for upload to complete
        time.sleep(10)
        logger.info("✅ Resume uploaded successfully!")

    except Exception as e:
        logger.error(f"❌ Error during resume upload: {e}")

    finally:
        driver.quit()
        logger.info("✅ Process completed successfully!")


if __name__ == "__main__":
    logger.info("Starting Resume Update Process...")

    if download_resume_from_s3():
        upload_resume_naukri()
