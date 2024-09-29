import os

import requests
import streamlit as st
from streamlit_elements import elements, mui

desired_nutrients = {
    "Energy": ("Energy", "KCAL"),
    "Total lipid (fat)": ("Fat", "G"),
    "Cholesterol": ("Cholesterol", "MG"),
    "Sodium, Na": ("Sodium", "MG"),
    "Carbohydrate, by difference": ("Carbohydrate", "G"),
    "Sugars, total including NLEA": ("Sugar", "G"),
    "Protein": ("Protein", "G"),
}

st.set_page_config(layout="wide")


def apply_custom_styles():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #395E66;
        }
        [data-testid="stSidebar"] {
            background-color: #204E4A;
        }
        [data-testid="stHeader"], [data-testid="stToolbar"], header {
            background-color: #395E66;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def preload_food_items(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            food_items = [item.strip() for item in content.split(",") if item.strip()]
            return food_items
    except FileNotFoundError:
        st.error(f"File {file_path} not found.")
        return []


def get_nutrition_data(food_item, api_key):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"query": food_item, "api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_nutrition_info(food_items, nutrition_results: dict, batch_size=2):
    nutrition_summary = {k: 0 for k in desired_nutrients}
    for nutrition_result in nutrition_results and nutrition_results.values():
        for nutrient, val in nutrition_result["nutrition"].items():
            nutrition_summary[nutrient] += val

    with elements("style_mui_sx"):
        with mui.Box(
            sx={
                "display": "flex",
                "flexDirection": "row",
                "overflowX": "auto",
                "padding": "10px",
                "gap": "10px",
                "backgroundColor": "#395E66",
                "borderRadius": "0",
            }
        ):
            with mui.Card(
                sx={
                    "bgcolor": "background.paper",
                    "boxShadow": 1,
                    "borderRadius": 2,
                    "p": 2,
                    "minWidth": 300,
                }
            ):
                mui.Typography("Summary", variant="h3")
                mui.Typography("infoinfo")
            pass
    # for i in range(0, len(food_items), batch_size):
    #     cols = st.columns(min(batch_size, len(food_items) - i))
    #     for index, food_item in enumerate(food_items[i : i + batch_size]):
    #         with cols[index]:
    #             if food_item in nutrition_results and nutrition_results[food_item]:
    #                 st.write(f"**Food**: {nutrition_results[food_item]['description']}")
    #                 st.write("**Nutrition Facts**:")
    #                 for nutrient, val in nutrition_results[food_item][
    #                     "nutrition"
    #                 ].items():
    #                     st.write(f"{nutrient}: {val} {desired_nutrients[nutrient][1]}")
    #                 st.write("\n")
    #             else:
    #                 st.error(f"No data found for {food_item}.")


if st.sidebar.toggle("Developer Mode", False):
    if st.sidebar.button("[DEBUG] Clear food.txt"):
        with open("food.txt", "w") as ff:
            ff.write("")
        st.sidebar.success("File contents cleared!")

    if st.sidebar.button("[DEBUG] Write to food.txt"):
        with open("food.txt", "w") as file:
            file.write("apple,pineapple")
        st.sidebar.success("Written 'apple,pineapple' to food.txt!")


def main():
    apply_custom_styles()

    st.sidebar.image("./web/plAIte.png", use_column_width=True, caption="plAIte")

    food_items = preload_food_items("food.txt")

    st.title("Nutrition Information Finder")
    food_items_input = st.text_area(
        "Enter additional food items (separated by commas):"
    )

    if food_items_input:
        additional_items = [
            item.strip() for item in food_items_input.split(",") if item.strip()
        ]
        food_items.extend(additional_items)

    food_items = [item for item in food_items if item]

    if food_items:
        nutrition_results = {}

        with st.spinner("Fetching nutrition information..."):
            for food_item in food_items:
                if food_item:
                    nutrition_data = get_nutrition_data(
                        food_item, os.getenv("USDA_APIKEY")
                    )
                    if nutrition_data and nutrition_data.get("foods"):
                        food = nutrition_data["foods"][0]
                        nutrition_results[food_item] = {
                            "description": food["description"],
                            "nutrition": {
                                nutrient["nutrientName"]: nutrient["value"]
                                for nutrient in food["foodNutrients"]
                                if nutrient["nutrientName"] in desired_nutrients
                            },
                        }
                    else:
                        nutrition_results[food_item] = None
        display_nutrition_info(food_items, nutrition_results)

    else:
        st.warning(
            "No food items found. Please add food items to 'food.txt' or enter them manually."
        )


if __name__ == "__main__":
    main()
