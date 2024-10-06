# temp.py

import pickle  # Ensure pickle is imported
from recommender import RecipeRecommender

def save_recommender_model():
    recommender = RecipeRecommender(
        recipe_file='recipes.csv',
        non_vegan_file='non_vegan_ingredients.txt',
        alternatives_file='nonvegan-alternatives.csv',
        mapping_file='mapping_dict.pkl',
        non_vegan_file_contents=[line.strip() for line in open('non_vegan_ingredients.txt', 'r')]
    )
    with open('recipe_recommender_model.pkl', 'wb') as f:
        pickle.dump(recommender, f)

save_recommender_model()
