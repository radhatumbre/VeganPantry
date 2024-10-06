# main.py

import pickle
import pandas as pd
from recommender import VeganRecipeRecommender

df = pd.read_csv('recipes.csv')
import ast
def safe_literal_eval(val):
    if val is None:
        return val
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

# Convert string representations of lists to actual lists
df['ingredients'] = df['ingredients'].apply(safe_literal_eval)


with open('mapping_dict.pkl', 'rb') as f:
    mapping_dict = pickle.load(f)

with open('non_vegan_ingredients.txt', 'r') as file:
    non_vegan_ingr = [line.strip() for line in file]

df_non_vegan_alter = pd.read_csv('nonvegan-alternatives.csv')

# Create an instance of VeganRecipeRecommender
recommender = VeganRecipeRecommender(df, mapping_dict, non_vegan_ingr, df_non_vegan_alter)

# Save the instance to a pickle file
with open('data/vegan_recipe_recommender.pkl', 'wb') as file:
    pickle.dump(recommender, file)

print("VeganRecipeRecommender instance saved to pickle file.")




# Load the instance from the pickle file
with open('data/vegan_recipe_recommender.pkl', 'rb') as file:
    loaded_recommender = pickle.load(file)

print("VeganRecipeRecommender instance loaded from pickle file.")


# Example usage
user_ingrs = ['lime', 'sesame oil','garlic', 'fish sauce', 'ginger','bell pepper','tofu','cashew cheese','honey','butter','chili paste']
recommended_recipes = loaded_recommender.recommend_recipes(user_ingrs)
print("Recommended Recipes:")
print(recommended_recipes)