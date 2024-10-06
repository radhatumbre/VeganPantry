from flask import Flask, request, jsonify
import pickle
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the pre-trained model
with open('recipe_recommender_model.pkl', 'rb') as f:
    recommender = pickle.load(f)

# Load ingredients from file
with open('all_ingredients.txt', 'r') as file:
    all_ingredients = file.read().splitlines()
    
with open('non_vegan_ingredients.txt', 'r') as file:
    non_vegan_ingr = file.read().splitlines()

df_non_vegan_alter = pd.read_csv('nonvegan-alternatives.csv')

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    query = request.args.get('query', '').lower()
    filtered_ingredients = [ing for ing in all_ingredients if query in ing.lower()]
    return jsonify(filtered_ingredients)

@app.route('/nonvegan_ingredients', methods=['GET'])
def get_nonvegan_ingredients():
    query = request.args.get('query', '').lower()
    filtered_ingredients = [ing for ing in non_vegan_ingr if query in ing.lower()]
    return jsonify(filtered_ingredients)

@app.route('/nonvegan_alternatives', methods=['GET'])
def get_nonvegan_alternatives():
    # Convert DataFrame to JSON
    json_data = df_non_vegan_alter.to_dict(orient='records')
    return jsonify(json_data)


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        user_ingrs = data.get('ingredients', [])
        print(f"Received ingredients: {user_ingrs}")
        print(type(user_ingrs))
        # Check if the recommender object and its method are functioning correctly
        if not hasattr(recommender, 'recommend_recipes'):
            raise RuntimeError("Recommender object is not properly initialized")

        recommended_recipes = recommender.recommend_recipes(user_ingrs)
        print(f"Recommended recipes: {recommended_recipes.head()}")

        result = recommended_recipes.to_dict(orient='records')
        return jsonify(result)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return str(e), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
