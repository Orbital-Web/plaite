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


# Center the title and text with custom CSS
st.markdown(
    """
    <style>
    .centered {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown(
    '<h1 class="centered">Nutrition Information Finder</h1>', unsafe_allow_html=True
)

food_items_input = st.text_area("Enter food items (separated by commas):")

if food_items_input:
    seen = set()
    food_items = []

    # Process food items
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

    # Use a spinner to indicate loading
    with st.spinner("Fetching nutrition data..."):
        if "food_data" not in st.session_state:
            st.session_state.food_data = {}
            # Preload nutrition data for all food items
            for food_item in food_items:
                nutrition_data = get_nutrition_data(food_item, API_KEY)
                if (
                    nutrition_data
                    and "foods" in nutrition_data
                    and nutrition_data["foods"]
                ):
                    st.session_state.food_data[food_item] = nutrition_data["foods"][0]
                else:
                    st.session_state.food_data[food_item] = None

    if "food_index" not in st.session_state:
        st.session_state.food_index = 0

    current_index = st.session_state.food_index

    # Center navigation buttons
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])

    # Navigation buttons for Previous and Next
    with col1:
        if st.button("Previous"):
            if current_index > 0:
                st.session_state.food_index -= 1

    with col3:
        if st.button("Next"):
            if current_index < len(food_items) - 1:
                st.session_state.food_index += 1
    st.markdown("</div>", unsafe_allow_html=True)

    # Display the data for the current food item
    current_food_item = food_items[st.session_state.food_index]
    food = st.session_state.food_data.get(current_food_item)

    if food:
        with st.container():
            st.markdown(
                f'<h2 class="centered">Food: {food["description"]}</h2>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<h3 class="centered">Nutrition Facts:</h3>', unsafe_allow_html=True
            )

            nutrition_list = []

            for desired_nutrient in desired_nutrients:
                for nutrient in food["foodNutrients"]:
                    if nutrient["nutrientName"] == desired_nutrient:
                        nutrition_list.append(
                            f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}"
                        )

            # Center the nutrition facts
            if nutrition_list:
                for line in nutrition_list:
                    st.markdown(
                        f"<p style='text-align: center;'>{line}</p>",
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No nutrition information available.")
    else:
        st.error(f"No data found for {current_food_item}.")
