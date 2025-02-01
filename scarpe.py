# Import necessary libraries
import json
import time
from datetime import datetime
import pandas as pd
import requests
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
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_path = ChromeDriverManager().install()
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver
    
def scrape_product_data(link):
    driver=get_driver()
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

# API keys
API_KEY = "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"  # Groq API Key
SLACK_WEBHOOK = "xoxe.xoxp-1-Mi0yLTgzNjMxNDY1MTEwMjgtODM3MzMxODc4NzI5Ny04Mzg1NTc0Mjg4ODUxLTgzODgxODkwNzUxMjQtOWVlODU0MzVhOWJiZjk3ZTAzM2JkNzdkNjVhNjE2MTViOTM3ZWRjMzc3MGRiYjI3ZDQ0MzhmM2FhNzNlYjkyZA"  # Slack webhook URL
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
    data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce")
    data = data.dropna(subset=["Discount"])

    discount_series = data["Discount"]

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

products = [
    "Apple iPhone 15",
    "Apple 2023 MacBook Pro",
    "OnePlus Nord 4 5G",
    "Sony WH-1000XM5"
]
selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)

competitor_data = load_competitor_data()
reviews_data = load_reviews_data()

product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews = reviews_data[reviews_data["product_name"] == selected_product]

st.header(f"Competitor Analysis for {selected_product}")
st.subheader("Competitor Data")
st.table(product_data.tail(5))

if not product_reviews.empty:
    product_reviews["reviews"] = product_reviews["reviews"].apply(
        lambda x: truncate_text(x, 512)
    )
    reviews = product_reviews["reviews"].tolist()
    sentiments = analyze_sentiment(reviews)

    st.subheader("Customer Sentiment Analysis")
    sentiment_df = pd.DataFrame(sentiments)
    fig = px.bar(sentiment_df, x="label", title="Sentiment Analysis Results")
    st.plotly_chart(fig)
else:
    st.write("No reviews available for this product.")

product_data["Date"] = pd.to_datetime(product_data["Date"], errors="coerce")
product_data = product_data.dropna(subset=["Date"])
product_data.set_index("Date", inplace=True)
product_data["Discount"] = pd.to_numeric(product_data["Discount"], errors="coerce")
product_data = product_data.dropna(subset=["Discount"])

# Forecasting Model
product_data_with_predictions = forecast_discounts_arima(product_data)

st.subheader("Competitor Current and Predicted Discounts")
st.table(product_data_with_predictions.tail(10))

recommendations = generate_strategy_recommendation(
    selected_product,
    product_data_with_predictions,
    sentiments if not product_reviews.empty else "No reviews available",
)

st.subheader("Strategic Recommendations")
st.write(recommendations)

send_to_slack(recommendations)
