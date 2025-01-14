# src/config.py
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ChromeDriver path
CHROMEDRIVER_PATH = r"C:\chromedriver-win64\chromedriver.exe"
INSTAGRAM_USERNAME = "Your insta profile"
INSTAGRAM_PASSWORD = "Your password"

# Instagram Base URL
BASE_URL = "https://www.instagram.com"

# Configure Selenium Chrome options
def get_chrome_options():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (optional)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options
