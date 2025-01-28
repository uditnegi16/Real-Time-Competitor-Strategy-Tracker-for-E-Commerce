import json
import time
from datetime import datetime


import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller

links={
    "Apple iPhone 13 (128GB) - Green":"https://www.amazon.in/Apple-iPhone-13-128GB-Green/dp/B09V4B6K53/ref=sr_1_1_sspa?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
    "Apple iPhone 14 (128 GB) - Midnight":"https://www.amazon.in/Apple-iPhone-14-128GB-Midnight/dp/B0BDHX8Z63/ref=sr_1_2_sspa?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
    "Apple iPhone 15 (128 GB) - Blue":"https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX2F5QT/ref=sr_1_3?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-3&th=1"
    }
def scrape_product_data(link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--lang=en')
    chrome_options.add_argument('--window-size=1920, 1080')

    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome(options = chrome_options)
    driver.set_window_size(1920, 1080)
    driver.get(link)
    product_data, review_data = {}, {}
    product_data["reviews"] = []
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    retry = 0
    while retry < 3:
        try:
            driver.save_screenshot("screenshot.png")
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-offscreen")))
            break

        except Exception:
            print("retrying")
            retry += 1
            driver.get(link)
            time.sleep(5)

        driver.save_screenshot("screenshot.png")


        try:
            price_elem = driver.find_element(By.XPATH,
            '// *[ @ id = "corePriceDisplay_desktop_feature_div"] / div[1] / span[3] / span[2] / span[2]',)
            product_data["selling price"] = int("".join(price_elem.text.strip().split(",")))

        except:
            product_data["selling price"] = 0

        try:
            original_price = driver.find_element(
                By.XPATH,
                '// * [ @ id = "corePriceDisplay_desktop_feature_div"] / div[2] / span / span[1] / span[2] / span /span[2]',).text

            product_data["original price"] = int("".join(original_price.strip().split(",")))
        except:
            product_data["original price"] = 0


        try:
            discount = driver.find_element(

                       By.XPATH,
        ' // *[ @ id = "corePriceDisplay_desktop_feature_div"] / div[1] / span[2] ',)
            full_rating_text = discount.get_attribute("innerHTML").strip()
            if " out of 5 stars" in full_rating_text.lower():
                product_data["rating"] = (
                        full_rating_text.lower().split(" out of")[0].strip()
                )
            else:
                product_data["discount"] = full_rating_text


        except:
            product_data["discount"] = 0

        try:
            driver.find_element(By.CLASS_NAME, "a-icon-popover").click()
            time.sleep(1)

        except:
            pass

        try:
            reviews_link = driver.find_elements(
            By.XPATH, "//a[contains(text(), 'See customer reviews')]")[-1].get_attribute("href")
            product_data["product_url"] = reviews_link.split("#")[0]
            driver.get(reviews_link)
            time.sleep(3)
            reviews = driver.find_element(By.ID, "cm-cr-dp-review-list")
            reviews = reviews.find_elements(By.TAG_NAME, "li")
            for item in reviews:
                product_data["reviews"].append(item.get_attribute("innerText"))
            driver.back()
            time.sleep(3)

        except Exception:
            product_data["reviews"] = []
            driver.quit()
            return product_data

for product_name, link in links.items():
    product_data = scrape_product_data(link)
    reviews = json.loads(pd.read_csv("reviews.csv").to_json(orient = "records"))
    price = json.loads(pd.read_csv("competitor_data.csv").to_json(orient="records"))
    price.append(
        {

            "product_name": product_name,
            "Price": product_data["product_name"],
            "Discount": product_data["discount"],
            "Date": datetime.now().strftime("%d-%m-%y"),
        }
    )
    for i in product_data["reviews"]:
        reviews.append({"product_name": product_name, "reviews": i})
    pd.DataFrame(reviews).to_csv("reviews.csv", index=False)
    pd.DataFrame(price).to_csv("competitor_data.csv", index=False)
