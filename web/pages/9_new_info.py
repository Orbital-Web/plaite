import os

import requests
import streamlit as st

API_KEY = os.getenv("USDA_APIKEY")


def get_nutrition_data(food_item, api_key):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"query": food_item, "api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


st.title("Nutrition Information Finder")
food_items_input = st.text_area("Enter food items (separated by commas):")

if food_items_input:
    seen = set()
    food_items = []

    for item in food_items_input.split(","):
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            food_items.append(item)

    desired_nutrients = [
        "Energy",
        "Total lipid (fat)",
        "Cholesterol",
        "Sodium, Na",
        "Carbohydrate, by difference",
        "Sugars, total including NLEA",
        "Protein",
    ]

    # Create a dictionary to store all the fetched nutrition data
    nutrition_results = {}

    with st.spinner("Fetching nutrition information..."):
        # Fetch data for all food items first
        for food_item in food_items:
            if food_item:
                nutrition_data = get_nutrition_data(food_item, API_KEY)
                if (
                    nutrition_data
                    and "foods" in nutrition_data
                    and nutrition_data["foods"]
                ):
                    food = nutrition_data["foods"][0]
                    nutrition_list = []

                    for desired_nutrient in desired_nutrients:
                        for nutrient in food["foodNutrients"]:
                            if nutrient["nutrientName"] == desired_nutrient:
                                nutrition_list.append(
                                    f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}"
                                )
                    nutrition_results[food_item] = {
                        "description": food["description"],
                        "nutrition": nutrition_list,
                    }
                else:
                    nutrition_results[food_item] = None

    # Display information in batches of 3 columns at a time
    batch_size = 2
    for i in range(0, len(food_items), batch_size):
        cols = st.columns(
            min(batch_size, len(food_items) - i)
        )  # Handle remaining items in the last batch
        for index, food_item in enumerate(food_items[i : i + batch_size]):
            with cols[index]:
                if nutrition_results[food_item]:
                    st.write(f"**Food**: {nutrition_results[food_item]['description']}")
                    st.write("**Nutrition Facts**:")
                    for line in nutrition_results[food_item]["nutrition"]:
                        st.write(line)
                    st.write("\n")
                else:
                    st.error("No data found.")
