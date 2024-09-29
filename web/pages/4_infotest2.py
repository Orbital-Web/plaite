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
        st.error(f"Error: {response.status_code}")
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

    cols = st.columns(len(food_items))

    for index, food_item in enumerate(food_items):
        if food_item:
            nutrition_data = get_nutrition_data(food_item, API_KEY)
            if nutrition_data and "foods" in nutrition_data and nutrition_data["foods"]:
                food = nutrition_data["foods"][0]

                with cols[index]:
                    st.write(f"**Food**: {food['description']}")
                    st.write("**Nutrition Facts**:")

                    nutrition_list = []

                    for desired_nutrient in desired_nutrients:
                        for nutrient in food["foodNutrients"]:
                            if nutrient["nutrientName"] == desired_nutrient:
                                nutrition_list.append(
                                    f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}"
                                )
                    if nutrition_list:
                        for line in nutrition_list:
                            st.write(line)
                        st.write("\n")
            else:
                st.error("No data found.")