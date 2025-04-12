from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path ke chromedriver
chrome_driver_path = "C:/Users/hp/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Setup WebDriver
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode (opsional)
options.add_argument("window-size=1920x1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
driver = webdriver.Chrome(service=service, options=options)

def scrape_reviews(start_page=1, end_page=500, file_output="all_reviwes.csv"):
    all_reviews = []

    for current_page in range(start_page, end_page + 1):
        page_url = f"https://www.trustpilot.com/review/flashbay.com?page={current_page}"
        print(f"🔎 Mengakses halaman {current_page}...")

        driver.get(page_url)
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "styles_reviewContent__SCYfD"))
            )
            reviews = driver.find_elements(By.CLASS_NAME, "styles_reviewContent__SCYfD")

            for review in reviews:
                try:
                    title = review.find_element(By.TAG_NAME, "h2").text
                except:
                    title = ""
                try:
                    content = review.find_element(By.TAG_NAME, "p").text
                except:
                    content = ""
                all_reviews.append({"title": title, "content": content})
        except Exception as e:
            print(f"❌ Gagal load halaman {current_page}: {e}")

        time.sleep(2)  # jeda untuk menghindari deteksi bot

    # Simpan ke CSV
    df = pd.DataFrame(all_reviews)
    df.to_csv(file_output, index=False)
    print(f"✅ Selesai scraping halaman {start_page}–{end_page}. Data disimpan di '{file_output}'")

# Jalankan scraper
scrape_reviews()

# Tutup browser
driver.quit()
