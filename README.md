# Real-Time Competitor Strategy Tracker for E-Commerce

## Project Overview
This project focuses on creating a real-time competitive intelligence tool for e-commerce businesses. It provides actionable insights by monitoring competitor pricing, discount strategies, and customer sentiment. The solution leverages:
- **Machine Learning**: Predictive modeling with ARIMA.
- **LLMs**: Sentiment analysis using Hugging Face Transformers and Groq.
- **Integration**: Slack notifications for real-time updates.

## Features
1. **Competitor Data Aggregation**: Track pricing and discount strategies.
2. **Sentiment Analysis**: Analyze customer reviews for actionable insights.
3. **Predictive Modeling**: Forecast competitor discounts.
4. **Slack Integration**: Get real-time notifications on competitor activity.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
Install the required Python libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
This project requires the following keys:
- **Groq API Key**: For generating strategic recommendations.
- **Slack Webhook URL**: For sending notifications.

### Steps:
1. **Groq API Key**:
   - Sign up for a Groq account at https://groq.com.
   - Obtain your API key from the Groq dashboard.
   - Use the API key in the `app.py` file.

2. **Slack Webhook Integration**:
   - Go to the [Slack API](https://api.slack.com/apps).
   - Create a new app and enable **Incoming Webhooks**.
   - Add a webhook to a channel and copy the generated URL.
   - Add this URL to the `app.py` file.


### 5. Run the Application
Run the Streamlit app:
```
streamlit run app.py
```

---

## Project Files
- **`app.py`**: Main application script.
- **`scrape.py`**: Script for web scraping competitor data.
- **`reviews.csv`**: Sample reviews data for sentiment analysis.
- **`competitor_data.csv`**: Sample competitor data for analysis.
- **`requirements.txt`**: List of dependencies.

---

## Usage
1. Launch the Streamlit app.
2. Select a product from the sidebar.
3. View competitor analysis, sentiment trends, and discount forecasts.
4. Get strategic recommendations and real-time Slack notifications.

---
