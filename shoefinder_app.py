#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 17:17:53 2023

@author: huiziyu
"""

from shoe_data_processor import ShoeDataProcessor
import streamlit as st
import itertools

# Set up API key, shoe types, and colors
api_key = "79cf37c845e6b957b3646abd88c9e138ebb038f2aae236a069260c442e27f0a8"
shoes_type = ["sneaker", "boots", "sandals", "loafers"]
colors = ["red", "black", "blue", "white", "pink"]

# Create an instance of ShoeDataProcessor with the provided parameters
processor = ShoeDataProcessor(api_key, shoes_type, colors)

# Load or fetch data from the cache
cached_data = processor.load_from_cache()
if cached_data is not None:
    # If data is cached, use the cached data
    all_results = cached_data
    print("Data loaded successfully")
else:
    # If no cached data, fetch shopping results for all combinations of shoe types and colors
    all_results = []
    for shoe, color in itertools.product(shoes_type, colors):
        shopping_results = processor.get_shopping_results(shoe, color)
        all_results.extend(shopping_results)
    # Save the fetched data to the cache
    processor.save_to_cache(all_results)

# Initialize Streamlit interface
st.set_page_config(layout="wide")

def main():
    # Set up the layout with two columns
    st.title("👟 Shoe Finder Application 👟")
    col1, col2 = st.columns([2, 3])

    # Column 1: Input Selection
    with col1:
        st.markdown("### Input Selection")
        # Build a hierarchical tree structure based on all results
        tree = processor.build_tree(all_results)
        # Allow the user to select options for shoe type, color, brand, price range, and rating
        shoe_type = st.selectbox("Choose Shoe Type", options=list(tree.keys()))
        color = st.selectbox("Choose Color", options=list(tree.get(shoe_type, {}).keys()))
        brand = st.selectbox("Choose Brand", options=list(tree.get(shoe_type, {}).get(color, {}).keys()))
        price_range = st.selectbox("Choose Price Range", options=list(tree.get(shoe_type, {}).get(color, {}).get(brand, {}).keys()))
        rating = st.selectbox("Choose Rating", options=list(tree.get(shoe_type, {}).get(color, {}).get(brand, {}).get(price_range, {}).keys()))

    # Column 2: Selection Results
    with col2:
        st.markdown("### Selection Results")
        # Retrieve the selected product based on user choices
        final_selection = tree.get(shoe_type, {}).get(color, {}).get(brand, {}).get(price_range, {}).get(rating, [])
        # Allow the user to select a product to view reviews
        selected_product = st.radio("Select a product to view reviews", final_selection, format_func=lambda x: x['title'])

        # Button to fetch reviews
        if st.button("Fetch Reviews"):
            if selected_product:
                # Display a link to the selected product's shop
                st.markdown(f"[Link to Shop]({selected_product['link']})")
                # Fetch and process reviews for the selected product
                reviews_data = processor.fetch_and_combine_reviews([selected_product])
                processed_reviews = processor.process_reviews(reviews_data)

                # Display reviews
                if processed_reviews:
                    review_info = processed_reviews[0]  # Assuming single selection
                    st.markdown("### Product Reviews")
                    st.markdown("#### Keywords")
                    st.write(", ".join(review_info['keywords']))
                    st.markdown("#### Top Reviews")
                    for key, review in review_info['top_five_reviews'].items():
                        st.markdown(f"**{key}**: {review}")
            else:
                st.write("No product selected.")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()