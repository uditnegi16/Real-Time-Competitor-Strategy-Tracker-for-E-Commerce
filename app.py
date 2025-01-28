import json
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from openai import AzureOpenAI
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from transformers import pipeline

API_KEY="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"#groq API KEY
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"#SLACK WEBHOOK URL

def truncate_text(text, max_length=512):
  return text[:max_length]

def load_competitor_data():
  """load competitor data from csv file"""
  data=pd.read_csv("competitor_data.csv")
  print(data.head())
  return data

def load_reviews_data():
  """load views data from a csv file"""
  reviews=pd.read_csv("reviews.csv")
  return reviews

def analyze_sentiment(reviews):
  """analyze customer sentiment for review"""
  sentiment_pipeline=pipeline("sentiment-analysis")
  return sentiment_pipeline(reviews)

def train_predictive_model(data):
  """trian a predictive model for comeptitor pricing strategy"""
  data["Discount"]=data["Discount"].str.replace("%","").astype(float)
  data["Price"]=data["Price"].astype(int)
  data["Predicted_Discount"]=data["Discount"]+(data["Price"] * 0.05).round(2)

  x=data[["Price", "Discount"]]
  y=data["Predicted_Discount"]
  print(x)
  x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.2, random_state=42, train_size=0.8)

  model=RandomForestRegressor(random_state=42)
  model.fit()
  return model

import numpy as np
import pandas as pd

def forecast_discounts_arima(data, future_days=5):
  """
  forecast future discountss using ARIMA
  :param data: Datsframe containing historical discount data(with a datetime indrex).
  :param future_days: number of days to forecast.
  :return: Dataframe withh historical and forecasted discounts.
  """

  data=data.sort_index()
  print(product_data.index)

  data["Discount"]=pd.to_numeric(data["Discount"], errors="coerce")
  data=data.dropna(subset=["Discount"])

  discount_series=data["Discount"]
  if not isinstance(data.index, pd.DatetimeIndex):
    try:
      data.index=pd.to_datetime(data.index)
    except Exception as e:
      raise ValueError(
          "index must be datetime or convertible to datetime"
      )from e

  model=ARIMA(discount_series, order=(5,1,0))
  model_fit=model.fit()

  forecast=model_fit.forecast(steps=future_days)

  future_dates=pd.date_range(
      start=discount_series.index[-1] + pd.Timedelta(days=1), periods=future_days
      )
  forecast_df=pd.DataFrame({"Date": future_dates, "Predicted_Discount": forecast})
  forecast_df.set_index("Date", inplace=True)
  return forecast_df
  
def send_to_slack(data):
  payload={"text": data}
  response=requests.post(
      SLACK_WEBHOOK,
      data=json.dumps(payload),
      headers={"content-type": "application/json"},
  )
def generate_strategy_recommendation(product_name, competitor_data, sentiment):
  """Generate strategic recommendations using an LLM."""
  date=datetime.now()
  prompt = f"""
  You are a highly skilled business strategist specializing in e-commerce. Based on the following details, sug

1.**Product Name**: {product_name}

2.**Competitor Data** (including current prices, discounts, and predicted discounts):

{competitor_data}

3.**Sentiment Analysis**:
{sentiment}

5.**Today's Date**: {str(date)}

###Task:

-Analyze the competitor data and identify key pricing trends.-

-Leverage sentiment analysis insights to highlight areas where customer satisfaction can be improved.

-Use the discount predictions to suggest how pricing strategies can be optimized over the next 5 days.

-Recommend promotional campaigns or marketing strategies that align with customer sentiments and competitive tr
-Ensure the strategies are actionable, realistic, and geared toward increasing customer satisfaction, driving s

Provide your recommendations in a structured format:


1. **pricing Strategy**

2. ***Promotional Campaign Ideas**

3. **Customer Satisfaction Recommendations*
    """
  messages = [{"role": "user", "content": prompt}]

  data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-8b-8192",
        "temperature": 0,
  }

  headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

  res = requests.post(
      "https://api.grog.com/openai/v1/chat/completions",
       data=json.dumps(data),
       headers=headers,
  )
  res=res.json()
  response=res["choices"][0]["message"]["content"]
  return response

st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")

st.title("E-Commerce Competitor Strategy Dashboard")

st.sidebar.header("Select a Product")

products = [
    "Apple iPhone 15",
    "Apple 2023 MacBook Pro (16-inch, Apple M3 Pro chip with 12-core CPU and 18-core GPU, 36GB Unified Memory, 512GB SSD)",
    "OnePlus Nord 4 5G (Mercurial Silver, 8GB RAM, 256GB Storage)",
    "Sony WH-1000XM5 Best Active Noise Cancelling Wireless Bluetooth Over Ear Headphones with Mic for Clear call"
]
selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)



competitor_data = load_competitor_data()
reviews_data = load_reviews_data()


product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews=reviews_data[reviews_data["product_name"] == selected_product]



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


#Preprocessing

product_data["Date"] = pd.to_datetime(product_data["Date"], errors="coerce")

product_data = product_data.dropna(subset=["Date"])

product_data.set_index("Date", inplace=True)

product_data = product_data.sort_index()

product_data["Discount"] = pd.to_numeric(product_data["Discount"], errors="coerce")

product_data = product_data.dropna(subset=["Discount"])

#Forecasting Model

product_data_with_predictions = forecast_discounts_arima(product_data)

st.subheader("Competitor Current and Predicted Discounts")
st.table(product_data_with_predictions.tail(10))

recommendations = generate_strategy_recommendation(
    selected_product,
    product_data_with_predictions,
    sentiment if not product_reviews.empty else "no reviews available",
    )
st.subheader("strategic recommendations")
st.write(recommendations)
send_to_slack(recommendations)
