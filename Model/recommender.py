# recommender.py

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast


def safe_literal_eval(val):
    if val is None:
        return val
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val


class VeganRecipeRecommender:
    def __init__(self, df, mapping_dict, non_vegan_ingr, df_non_vegan_alter):
        self.df = df
        self.mapping_dict = mapping_dict
        self.non_vegan_ingr = non_vegan_ingr
        self.df_non_vegan_alter = df_non_vegan_alter
        self.vectorizer = None

    def extract_base_ingr(self, ingredients_list, instructions):
        base_ingr = []
        for ingr in ingredients_list:
            ingr = ingr.lower()
            found = False
            for key in self.mapping_dict:
                if found:
                    break
                if key.lower() in ingr:
                    found = True
                    base_ingr.append(self.mapping_dict[key].lower())
        # Remove duplicates
        seen = set()
        base_ingr = [x for x in base_ingr if not (x in seen or seen.add(x))]
        return base_ingr

    def base_instructions(self, instructions, ingredients_list):
        for ingr in ingredients_list:
            ingr = ingr.lower()
            found = False
            for key in self.mapping_dict:
                if found:
                    break
                if key.lower() in ingr:
                    found = True
                    instructions = instructions.replace(key.lower(), self.mapping_dict[key].lower())
        return instructions

    def conver_to_vegan(self, ingr_list):
        vegan_list = []
        for i in ingr_list:
            if i in self.non_vegan_ingr:
                filtered_df = self.df_non_vegan_alter[self.df_non_vegan_alter['BaseIngredient'] == i]
                vegan_alternatives = filtered_df['VeganAlternative']
                result_list = [item.strip() for sublist in vegan_alternatives.str.split(',') for item in sublist]
                for alter in result_list:
                    vegan_list.append(alter)
            else:
                vegan_list.append(i)
        return vegan_list

    def vegan_with_available(self, ingr_list, user_ingrs):
        vegan_list = []
        for i in ingr_list:
            if i in self.non_vegan_ingr:
                filtered_df = self.df_non_vegan_alter[self.df_non_vegan_alter['BaseIngredient'] == i]
                vegan_alternatives = filtered_df['VeganAlternative']
                result_list = [item.strip() for sublist in vegan_alternatives.str.split(',') for item in sublist]
                found = False
                for alter in result_list:
                    if alter in user_ingrs:
                        vegan_list.append(alter)
                        found = True
                        break
                if not found:
                    vegan_list.append(result_list[0])
            else:
                vegan_list.append(i)
        return ', '.join(vegan_list)

    def instructions_with_vegan_available(self, instructions, ingr_list, user_ingrs):
        for i in ingr_list:
            if i in self.non_vegan_ingr:
                filtered_df = self.df_non_vegan_alter[self.df_non_vegan_alter['BaseIngredient'] == i]
                vegan_alternatives = filtered_df['VeganAlternative']
                result_list = [item.strip() for sublist in vegan_alternatives.str.split(',') for item in sublist]
                found = False
                for alter in result_list:
                    if alter in user_ingrs:
                        instructions = instructions.replace(i, alter)
                        found = True
                        break
                if not found:
                    instructions = instructions.replace(i, result_list[0])
        return instructions

    def recommend_recipes(self, user_ingrs):
        # Process base ingredients and instructions
        self.df['base_ingredients'] = self.df.apply(
            lambda row: self.extract_base_ingr(row['ingredients'], row['instructions']), axis=1)
        self.df['instructions'] = self.df.apply(
            lambda row: self.base_instructions(row['instructions'], row['ingredients']), axis=1)

        # Convert to vegan ingredients
        self.df['vegan_ingredients'] = self.df['base_ingredients'].apply(self.conver_to_vegan)

        # Filter recipes with at least 3 matching ingredients
        self.df['HasEnoughIngredients'] = self.df['vegan_ingredients'].apply(
            lambda x: self.check_ingredients(x, user_ingrs))
        suitable_recipes = self.df[self.df['HasEnoughIngredients']]

        # Adjust vegan ingredients with available user ingredients
        suitable_recipes['tags'] = suitable_recipes['base_ingredients'].apply(
            lambda x: self.vegan_with_available(x, user_ingrs))

        # Update instructions with vegan alternatives available to the user
        suitable_recipes['instructions'] = suitable_recipes.apply(
            lambda row: self.instructions_with_vegan_available(row['instructions'], row['base_ingredients'],
                                                               user_ingrs), axis=1)

        # Create ingredient matrix for similarity calculation
        self.vectorizer = CountVectorizer(tokenizer=lambda x: x.split(', '))
        X = self.vectorizer.fit_transform(suitable_recipes['tags'])

        # Calculate cosine similarity between user ingredients and recipes
        user_vector = self.vectorizer.transform([', '.join(user_ingrs)])
        similarities = cosine_similarity(user_vector, X).flatten()

        # Add similarity scores and sort recipes by similarity
        suitable_recipes['Similarity'] = similarities
        # recommended_recipes = suitable_recipes.sort_values(by='Similarity', ascending=False)
        recommended_recipes = suitable_recipes.sort_values(by='Similarity', ascending=False).head(100)

        return recommended_recipes

    def check_ingredients(self, recipe_ingredients, user_ingredients):
        recipe_ingredients_set = set(recipe_ingredients)
        common_ingredients = recipe_ingredients_set.intersection(user_ingredients)
        return len(common_ingredients) >= 3
