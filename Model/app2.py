import streamlit as st
import pickle
import pandas as pd
import ast
from recommender2 import VeganRecipeRecommender

# Set page configuration for full-width layout
st.set_page_config(layout="wide")

# Load data and recommender
@st.cache_resource
def load_data():
    df = pd.read_csv('recipes.csv')
    df['ingredients'] = df['ingredients'].apply(safe_literal_eval)

    with open('mapping_dict.pkl', 'rb') as f:
        mapping_dict = pickle.load(f)

    with open('non_vegan_ingredients.txt', 'r') as file:
        non_vegan_ingr = [line.strip() for line in file]

    df_non_vegan_alter = pd.read_csv('nonvegan-alternatives.csv')

    recommender = VeganRecipeRecommender(df, mapping_dict, non_vegan_ingr, df_non_vegan_alter)

    return recommender

def safe_literal_eval(val):
    if val is None:
        return val
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

# Load the recommender instance
recommender = load_data()

# Streamlit application
st.title('Vegan Recipe Recommender')

# Input for user ingredients
user_ingrs = st.text_area(
    "Enter your ingredients (comma-separated):",
    "lime, sesame oil, garlic, fish sauce, ginger, bell pepper, tofu, cashew cheese, honey, butter, chili paste"
)

# Process the input and display recipes
if st.button('Recommend Recipes'):
    user_ingrs_list = [ingr.strip() for ingr in user_ingrs.split(',')]
    recommended_recipes = recommender.recommend_recipes(user_ingrs_list)

    if not recommended_recipes.empty:
        st.write("Recommended Recipes:")

        # Create columns dynamically based on the number of recipes
        num_recipes = len(recommended_recipes)
        num_columns = min(num_recipes, 6)  # Adjust the number of columns if needed

        # Display recipes in a grid
        cols = st.columns(num_columns)

        for index, row in recommended_recipes.iterrows():
            col_index = index % num_columns
            with cols[col_index]:  # Cycle through columns
                st.image(row['images'], use_column_width=True)
                if st.button(row['title'], key=f"recipe_{index}"):
                    st.session_state.selected_recipe = row
                    st.st.rerun()

# Display instructions if a recipe is selected
if 'selected_recipe' in st.session_state:
    selected_recipe = st.session_state.selected_recipe
    st.write(f"### {selected_recipe['title']}")
    st.image(selected_recipe['images'], use_column_width=True)
    st.write("#### Instructions:")
    st.write(selected_recipe['instructions'])
else:
    st.write("Select a recipe to see the instructions.")
