import requests

API_KEY = "V66wlt62Gua5HkEGmADb3MedxUwKEZaUVpYgFxp9"


def get_nutrition_data(food_item, api_key):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {"query": food_item, "api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None


food_item = "chocolate ice cream"
nutrition_data = get_nutrition_data(food_item, API_KEY)

desired_nutrients = [
    "Energy",
    "Total lipid (fat)",
    "Cholesterol",
    "Sodium, Na",
    "Carbohydrate, by difference",
    "Sugars, total including NLEA",
    "Protein",
]

if nutrition_data:
    food = nutrition_data["foods"][0]
    print(f"Food: {food['description']}")
    print("Nutrition Facts:")
    for desired_nutrient in desired_nutrients:
        for nutrient in food["foodNutrients"]:
            if nutrient["nutrientName"] == desired_nutrient:
                print(
                    f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}"
                )
else:
    print("No data found")
