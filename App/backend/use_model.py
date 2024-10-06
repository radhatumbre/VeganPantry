# usage.py

import pickle
from recommender import RecipeRecommender

with open('recipe_recommender_model.pkl', 'rb') as f:
    recommender = pickle.load(f)

# user_ingrs = ['garlic', 'ginger', 'bell pepper', 'tofu', 'vegan cheese', 'onion', 'tomato', 'chili flakes']
user_ingrs = ['sugar', 'brown sugar','vanilla extract','honey','cream cheese','butter','baking soda','chocolate chips']
# garlic, ginger, bell pepper, tofu, vegan cheese, onion, tomato, chili flakes
recommended_recipes = recommender.recommend_recipes(user_ingrs)

print("Recommended Recipes:")
print(recommended_recipes)
