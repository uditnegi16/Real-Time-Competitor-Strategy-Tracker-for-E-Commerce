# Import necessary libraries
import json
import time
from datetime import datetime
import pandas as pd
import requests
import plotly.express as px  
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
from transformers import pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from selenium.webdriver.chrome.service import Service

links={
    "Apple iPhone 13 (128GB) - Green":"https://www.amazon.in/Apple-iPhone-13-128GB-Green/dp/B09V4B6K53/ref=sr_1_1_sspa?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
    "Apple iPhone 14 (128 GB) - Midnight":"https://www.amazon.in/Apple-iPhone-14-128GB-Midnight/dp/B0BDHX8Z63/ref=sr_1_2_sspa?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
    "Apple iPhone 15 (128 GB) - Blue":"https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX2F5QT/ref=sr_1_3?crid=2XWF6OQBE9MW2&dib=eyJ2IjoiMSJ9.4Amcm6ymShwYf2cUNy6g87ZAmr160niWSMsGfJ6ktkhVvBfKClhwZifyFoyaaxp3p9CgrK4JD0kka6vg2gnarqoOb62duNBPCD13Tp0i69vRDmk4uzfDB-25bgoJNhIMNFEoNjBAjmfxVst_C0QmW8zulZt3XeCwXmXb04f26KHMlZ8v3WYOdj3IywjwNuQ1kRaqWcGGKYG5719prdWaQTuqcco0NBNjnzPCNlPyH_Y.GrzT8mZU2IyaErRyD0CZZeRLmD9_fnsrr95RqbZorhw&dib_tag=se&keywords=iphone&qid=1737998659&sprefix=iphone%2Caps%2C238&sr=8-3&th=1"
    }
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Automatically install the chromedriver version that matches the chromium version
    chromedriver_autoinstaller.install()

    # Create the webdriver with the options and use the default path
    driver = webdriver.Chrome(options=chrome_options)
    return driver

    
def scrape_product_data(link):
    driver = get_driver()
    driver.set_window_size(1920, 1080)
    driver.get(link)
    product_data = {
        "product_name": "",  # Add product_name to the dictionary
        "selling price": 0,
        "original price": 0,
        "discount": 0,
        "rating": 0,
        "reviews": [],
        "product_url": link,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    retry = 0
    while retry < 3:
        try:
            driver.save_screenshot("screenshot.png")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-offscreen")))
            break
        except Exception as e:
            print(f"Retrying... Error: {e}")
            retry += 1
            driver.get(link)
            time.sleep(5)

    try:
        price_elem = driver.find_element(
            By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'
        )
        product_data["selling price"] = int("".join(price_elem.text.strip().split(",")))
    except Exception as e:
        print(f"Error extracting selling price: {e}")

    try:
        original_price = driver.find_element(
        By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span[2]/span/span[2]'
        ).text
        product_data["original price"] = extract_price(original_price)
    except Exception as e:
        print(f"Error extracting original price: {e}")


    try:
        discount = driver.find_element(
            By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]'
        )
        full_rating_text = discount.get_attribute("innerHTML").strip()
        if " out of 5 stars" in full_rating_text.lower():
            product_data["rating"] = full_rating_text.lower().split(" out of")[0].strip()
        else:
            product_data["discount"] = full_rating_text
    except Exception as e:
        print(f"Error extracting discount: {e}")

    try:
        rating_elem = driver.find_element(By.CLASS_NAME, "a-icon-star")
        product_data["rating"] = rating_elem.get_attribute("innerText").strip()
    except Exception as e:
        print(f"Error extracting rating: {e}")
    try:
        reviews_link_elements = driver.find_elements(
        By.XPATH, "//a[contains(text(), 'See customer reviews')]"
        )
        if reviews_link_elements:
            reviews_link = reviews_link_elements[-1].get_attribute("href")
            driver.get(reviews_link)
            time.sleep(3)

            reviews_section = driver.find_element(By.ID, "cm-cr-dp-review-list")
            review_elements = reviews_section.find_elements(By.TAG_NAME, "li")

            for review in review_elements:
                product_data["reviews"].append(review.text.strip())
        else:
            print("No customer reviews found.")
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        
    driver.quit()
    return product_data

import re

def extract_price(price_text):
    """Extracts and converts price from a string with currency symbols or commas."""
    price_text = re.sub(r"[^\d]", "", price_text)  # Remove ₹, commas, and other symbols
    return int(price_text) if price_text else 0

def extract_rating_from_review(review_text):
    match = re.search(r"(\d+\.\d+) out of 5 stars", review_text)
    if match:
        return float(match.group(1))
    return None

for product_name, link in links.items():
    product_data = scrape_product_data(link)
    
    # Update reviews.csv
    try:
        reviews_df = pd.read_csv("reviews.csv")
    except FileNotFoundError:
        reviews_df = pd.DataFrame(columns=["product_name", "review", "rating", "date"])
    
    new_reviews = []
    for review_text in product_data["reviews"]:
        rating = extract_rating_from_review(review_text)
        new_reviews.append({
            "product_name": product_name,
            "review": review_text,
            "rating": rating,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    
    new_reviews_df = pd.DataFrame(new_reviews)
    reviews_df = pd.concat([reviews_df, new_reviews_df], ignore_index=True)
    reviews_df.to_csv("reviews.csv", index=False)
    
    # Update competitor_data.csv
    # try:
    #     competitor_df = pd.read_csv("competitor_data.csv")
    # except FileNotFoundError:
    #     competitor_df = pd.DataFrame(columns=["product_name", "price", "discount", "date"])
    
    # new_data = {
    #     "product_name": product_name,
    #     "price": product_data["selling price"],
    #     "discount": product_data["discount"],
    #     "date": datetime.now().strftime("%Y-%m-%d")
    # }
    
    # new_data_df = pd.DataFrame([new_data])
    # competitor_df = pd.concat([competitor_df, new_data_df], ignore_index=True)
    # competitor_df.to_csv("competitor_data.csv", index=False)
    try:
        competitor_df = pd.read_csv("competitor_data.csv")

        # Drop extra columns if they exist
        competitor_df = competitor_df[['product_name', 'price', 'discount', 'date']]
    except FileNotFoundError:
        competitor_df = pd.DataFrame(columns=["product_name", "price", "discount", "date"])

    # Create new data entry
    new_data = {
        "product_name": product_name,
        "price": product_data["selling price"],
        "discount": product_data["discount"],
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    #  Convert to DataFrame and ensure column alignment
    new_data_df = pd.DataFrame([new_data], columns=["product_name", "price", "discount", "date"])

    # Append data correctly
    competitor_df = pd.concat([competitor_df, new_data_df], ignore_index=True)

    # Save without extra columns
    competitor_df.to_csv("competitor_data.csv", index=False)

    
# API keys
API_KEY = "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"  # Groq API Key
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"  # Slack webhook URL
# Streamlit app setup
st.set_page_config(layout="wide")
# Create two columns
col1, col2 = st.columns(2)

# Add content to the first column
with col1:
     st.markdown(
        """
        <div style="font-size: 40px; text-align: left; width: 100%;">
            ❄️❄️❄️<strong>E-Commerce Competitor Strategy Dashboard</strong>❄️❄️❄️
        </div>
        """,
        unsafe_allow_html=True,
    )

# Add GIF to the second column
with col2:
    st.markdown(
        """
        <div style="text-align: right;">
            <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzh4dXpuc2hpY3JlNnR1MDdiMXozMXlreHFoZjl0a2g5anJqNWxtMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hWe6YajFuxX41eV8I0/giphy.gif" alt="Engaging GIF" width="300">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Utility function to truncate text
def truncate_text(text, max_length=512):
    return text[:max_length]

# Load competitor data
def load_competitor_data():
    """Load competitor data from a CSV file."""
    data = pd.read_csv("competitor_data.csv")
    st.write(data.head())  # Display data for debugging
    return data

# Load reviews data
def load_reviews_data():
    """Load reviews data from a CSV file."""
    reviews = pd.read_csv("reviews.csv")
    return reviews

# Analyze customer sentiment
def analyze_sentiment(reviews):
    """Analyze customer sentiment for reviews."""
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(reviews)

# Train predictive model
def train_predictive_model(data):
    """Train a predictive model for competitor pricing strategy."""
    data["Discount"] = data["Discount"].str.replace("%", "").astype(float)
    data["Price"] = data["Price"].astype(float)
    data["Predicted_Discount"] = data["Discount"] + (data["Price"] * 0.05).round(2)

    X = data[["Price", "Discount"]]
    y = data["Predicted_Discount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

# Forecast discounts using ARIMA
def forecast_discounts_arima(data, future_days=5):
    """
    Forecast future discounts using ARIMA.
    :param data: DataFrame containing historical discount data (with a datetime index).
    :param future_days: Number of days to forecast.
    :return: DataFrame with historical and forecasted discounts.
    """
    data = data.sort_index()
    data["discount"] = pd.to_numeric(data["discount"], errors="coerce")
    data = data.dropna(subset=["discount"])

    discount_series = data["discount"]

    if not isinstance(data.index, pd.DatetimeIndex):
        try:
            data.index = pd.to_datetime(data.index)
        except Exception as e:
            raise ValueError("Index must be datetime or convertible to datetime.") from e

    model = ARIMA(discount_series, order=(5, 1, 0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=future_days)
    future_dates = pd.date_range(
        start=discount_series.index[-1] + pd.Timedelta(days=1),
        periods=future_days
    )

    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Discount": forecast})
    forecast_df.set_index("Date", inplace=True)
    return forecast_df

# Send notifications to Slack
def send_to_slack(data):
    payload = {"text": data}
    response = requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    if response.status_code != 200:
        st.write(f"Failed to send notification to Slack: {response.status_code}")

# Generate strategy recommendations using an LLM
def generate_strategy_recommendation(product_name, competitor_data, sentiment):
    """Generate strategic recommendations using an LLM."""
    date = datetime.now()
    prompt = f"""
    You are a highly skilled business strategist specializing in e-commerce. Based on the following details, suggest actionable strategies:

    *Product Name*: {product_name}
    *Competitor Data* (including current prices, discounts, and predicted discounts):
    {competitor_data}
    *Sentiment Analysis*: {sentiment}
    *Today's Date*: {str(date)}

    # Task:
    - Analyze the competitor data and identify key pricing trends.
    - Leverage sentiment analysis insights to highlight areas where customer satisfaction can be improved.
    - Use the discount predictions to suggest how pricing strategies can be optimized over the next 5 days.
    - Recommend promotional campaigns or marketing strategies that align with customer sentiments and competitive trends.

    Provide your recommendations in a structured format:
    - **Pricing Strategy**
    - **Promotional Campaign Ideas**
    - **Customer Satisfaction Recommendations**
    """

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-8b-8192",
        "temperature": 0,
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(data),
        headers=headers,
    )
    res = res.json()
    response = res["choices"][0]["message"]["content"]
    return response

# Streamlit UI

st.sidebar.header("❄️Select a Product❄️")

def get_product_list():
    try:
        competitor_df = pd.read_csv("competitor_data.csv")
        return competitor_df["product_name"].drop_duplicates().tolist()
    except FileNotFoundError:
        return []

products = get_product_list()

selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)

competitor_data = load_competitor_data()
reviews_data = load_reviews_data()

product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews = reviews_data[reviews_data["product_name"] == selected_product]

st.header(f"Competitor Analysis for {selected_product}")
st.subheader("Competitor Data")
st.table(product_data.tail(5))

if not product_reviews.empty:
    product_reviews.loc[:, "review"] = product_reviews["review"].apply(lambda x: truncate_text(x, 512))

    reviews = product_reviews["review"].tolist()
    sentiments = analyze_sentiment(reviews)

    st.subheader("Customer Sentiment Analysis")
    sentiment_df = pd.DataFrame(sentiments)
    fig = px.bar(sentiment_df, x="label", title="Sentiment Analysis Results")
    st.plotly_chart(fig)
else:
    st.write("No reviews available for this product.")

product_data["date"] = pd.to_datetime(product_data["date"], errors="coerce")
# product_data = product_data.dropna(subset=["Date"])
product_data.index= pd.date_range(start=product_data.index.min(), periods=len(product_data), freq="D")
product_data["discount"] = pd.to_numeric(product_data["discount"], errors="coerce")
product_data = product_data.dropna(subset=["discount"])

# Forecasting Model
product_data_with_predictions = forecast_discounts_arima(product_data)

st.subheader("Competitor Current and Predicted Discounts")
st.table(product_data_with_predictions[["Predicted_Discount"]].tail(10))


recommendations = generate_strategy_recommendation(
    selected_product,
    product_data_with_predictions,
    sentiments if not product_reviews.empty else "No reviews available",
)
st.subheader("Strategic Recommendations")
st.write(recommendations)

send_to_slack(recommendations)
