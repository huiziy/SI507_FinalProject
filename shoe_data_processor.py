#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 17:16:24 2023

@author: huiziyu
"""

from serpapi import GoogleSearch
import pickle
import os
from IPython.display import HTML, display
import tabulate

class ShoeDataProcessor:
    """
        Initialize the ShoeDataProcessor object.

        Parameters:
        - api_key (str): The API key for accessing the Google Search API.
        - shoes_type (list): List of shoe types to consider.
        - colors (list): List of colors to consider.
    """
    def __init__(self, api_key, shoes_type, colors):
        self.api_key = api_key
        self.shoes_type = shoes_type
        self.colors = colors

    def get_shopping_results(self, shoe_type, color):
        """
        Get shopping results for a specific shoe type and color.

        Parameters:
        - shoe_type (str): The type of shoe.
        - color (str): The color of the shoe.

        Returns:
        - list: A list of dictionaries containing shopping results.
        """
        query = f"{shoe_type} {color}"
        print(query)
        params = {
            "api_key": self.api_key,
            "engine": "google_shopping",
            "q": query,
            "google_domain": "google.com"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        raw_shopping_results = results.get('shopping_results', [])

        shopping_results = []
        for result in raw_shopping_results:
            filtered_result = {
                'shoe_type': shoe_type,
                'color': color,
                'title': result.get('title', ''),
                'product_id': result.get('product_id', ''),
                'link': result.get('link', ''),
                'source': result.get('source', ''),
                'extracted_price': result.get('extracted_price', ''),
                'rating': result.get('rating', ''),
                'reviews': result.get('reviews', '')
            }
            shopping_results.append(filtered_result)

        return shopping_results

    def save_to_cache(self, data, filename='shoes_data_cache.pkl'):
        """
        Save data to a cache file.

        Parameters:
        - data: The data to be saved.
        - filename (str): The name of the cache file.
        """
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def load_from_cache(self, filename='data_cache.pkl'):
        """
        Load data from a cache file.

        Parameters:
        - filename (str): The name of the cache file.

        Returns:
        - object: The loaded data or None if the file does not exist.
        """
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        else:
            return None

    def categorize_price(self, price):
        """
        Categorize the price into predefined ranges.

        Parameters:
        - price (float/str): The price to be categorized.

        Returns:
        - str: The categorized price range.
        """
        try:
            price = float(price)
        except ValueError:
            return 'Unknown'
        if price <= 50:
            return 'Low (Under $50)'
        elif 51 <= price <= 100:
            return 'Medium (Between $50 and $100)'
        else:
            return 'High (Above $100)'

    def categorize_rating(self, rating):
        """
        Categorize the rating into predefined ranges.

        Parameters:
        - rating (float/str): The rating to be categorized.

        Returns:
        - str: The categorized rating.
        """
        try:
            rating = float(rating)
        except ValueError:
            return 'Unknown'
        
        if rating <= 1:
            return '1 Star'
        elif 1 < rating <= 2:
            return '2 Star'
        elif 2 < rating <= 3:
            return '3 Star'
        elif 3 < rating <= 4:
            return '4 Star'
        else:
            return '5 Star'

    def build_tree(self, data):
        """
        Build a hierarchical tree structure based on the input data.

        Parameters:
        - data (list): The input data containing shoe information.

        Returns:
        - dict: The hierarchical tree structure.
        """
        tree = {}
        for item in data:
            shoe_type = item['shoe_type']
            color = item.get('color', 'Unknown')
            brand = item['source']
            price_range = self.categorize_price(item['extracted_price'])
            rating = self.categorize_rating(item['rating'])
            product_id = item.get('product_id', '')
    
            tree.setdefault(shoe_type, {}) \
                .setdefault(color, {}) \
                .setdefault(brand, {}) \
                .setdefault(price_range, {}) \
                .setdefault(rating, []) \
                .append({'title': item['title'], 'link': item['link'], 'product_id': product_id})
    
        return tree


    def display_tree(self, tree):
        """
        Display the hierarchical tree structure.

        Parameters:
        - tree (dict): The hierarchical tree structure.
        """
        rows = []
        for shoe_type, colors in tree.items():
            for color, brands in colors.items():
                for brand, prices in brands.items():
                    for price, ratings in prices.items():
                        for rating, shoes in ratings.items():
                            for shoe in shoes:
                                link = f"<a href='{shoe['link']}' target='_blank'>{shoe['title']}</a>"
                                rows.append([shoe_type, color, brand, price, rating, link])
        display(HTML(tabulate.tabulate(rows, tablefmt='html', headers=["Shoe Type", "Color", "Brand", "Price Range", "Rating", "Link"])))
        
    def fetch_and_combine_reviews(self, selected_products):
        """
        Fetch and combine reviews for selected products.

        Parameters:
        - selected_products (list): List of selected products.

        Returns:
        - dict: Combined reviews data for the selected products.
        """
        combined_reviews = {}
        for item in selected_products:
            product_id = item.get('product_id', '')
            if product_id:
                params = {
                    "engine": "google_product",
                    "product_id": product_id,
                    "reviews": "1",
                    "gl": "us",
                    "hl": "en",
                    "api_key": self.api_key
                }
                search = GoogleSearch(params)
                try:
                    results = search.get_dict()
                    reviews_results = results.get("reviews_results", [])
                    combined_reviews[product_id] = reviews_results
                except Exception as e:
                    print(f"An error occurred while fetching reviews for product ID {product_id}: {e}")
            else:
                print(f"Product ID not found for item: {item}")
        return combined_reviews


    def process_reviews(self, reviews_data):
        """
        Process reviews data and extract relevant information.

        Parameters:
        - reviews_data (dict): Reviews data for products.

        Returns:
        - list: Processed reviews data.
        """
        processed_data = []
    
        for product_id, data in reviews_data.items():
            if data == []:
                processed_data.append({
                    'product_id': product_id,
                    'keywords': ["No Review Found"],
                    'top_five_reviews': {"Review_1": "No Review Found"}
                })
                continue
    
            processed_item = {
                'product_id': product_id,
                'keywords': [],
                'top_five_reviews': {}
            }
    
            filters = data.get('filters', [])
            for filter_item in filters:
                label = filter_item.get('label', '')
                processed_item['keywords'].append(label)
    
            reviews = data.get('reviews', [])
            for i, review in enumerate(reviews[:5]):
                title = review.get('title', '')
                content = review.get('content', '').replace('\xa0', ' ').strip()
                processed_item['top_five_reviews'][f'Review_{i+1}'] = f"{title} {content}"
    
            processed_data.append(processed_item)
    
        return processed_data
