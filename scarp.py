import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random

def scrape_product_data(url):
    """Scrape product data from e-commerce website."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product details
        product_name = soup.find('span', {'class': 'product-title'}).text.strip()
        price = float(soup.find('span', {'class': 'price'}).text.replace('₹', '').replace(',', '').strip())
        discount = float(soup.find('span', {'class': 'discount'}).text.replace('%', '').strip())
        
        # Get reviews if available
        reviews = []
        review_elements = soup.find_all('div', {'class': 'review'})
        for review in review_elements[:5]:  # Get latest 5 reviews
            review_text = review.find('p').text.strip()
            rating = float(review.find('span', {'class': 'rating'}).text.strip())
            reviews.append({
                'review_text': review_text,
                'rating': rating,
                'date': datetime.now().strftime('%Y-%m-%d')
            })
        
        return {
            'product_data': {
                'product_name': product_name,
                'price': price,
                'discount': discount,
                'date': datetime.now().strftime('%Y-%m-%d')
            },
            'reviews': reviews
        }
        
    except Exception as e:
        print(f"Error scraping data: {str(e)}")
        return None

def update_csv_files(product_data, reviews):
    """Update CSV files with new data."""
    # Update competitor_data.csv
    try:
        df_products = pd.DataFrame([product_data])
        df_products.to_csv('competitor_data.csv', mode='a', header=False, index=False)
        
        # Update reviews.csv
        if reviews:
            df_reviews = pd.DataFrame(reviews)
            df_reviews.to_csv('reviews.csv', mode='a', header=False, index=False)
            
        return True
    except Exception as e:
        print(f"Error updating CSV files: {str(e)}")
        return False

def main():
    # List of competitor URLs to monitor
    competitor_urls = [
        'https://example.com/product1',
        'https://example.com/product2',
        # Add more URLs as needed
    ]
    
    while True:
        for url in competitor_urls:
            data = scrape_product_data(url)
            if data:
                update_csv_files(data['product_data'], data['reviews'])
            
            # Random delay between requests (2-5 seconds)
            time.sleep(random.uniform(2, 5))
        
        # Wait for 1 hour before next update
        time.sleep(3600)

if __name__ == "__main__":
    main()
