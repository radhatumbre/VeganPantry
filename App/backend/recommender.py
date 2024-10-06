# recommender.py

import pandas as pd
import numpy as np
import pickle
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeRecommender:
    def __init__(
        self,
        recipe_file,
        non_vegan_file,
        alternatives_file,
        mapping_file,
        non_vegan_file_contents,
    ):
        self.df = pd.read_csv(recipe_file)
        self.non_vegan_ingr = non_vegan_file_contents
        self.df_non_vegan_alter = pd.read_csv(alternatives_file)
        with open(mapping_file, "rb") as f:
            self.mapping_dict = pickle.load(f)
        self._preprocess()

    def _preprocess(self):
        def safe_literal_eval(val):
            if val is None:
                return val
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                return val

        self.df["ingredients"] = self.df["ingredients"].apply(safe_literal_eval)

        def extract_base_ingr(ingredients_list):
            base_ingr = []
            for ingr in ingredients_list:
                if ingr is None:  # Check if ingr is None
                    continue
                ingr = ingr.lower()
                found = False
                for key in self.mapping_dict:
                    if found:
                        break
                    if key.lower() in ingr:
                        found = True
                        base_ingr.append(self.mapping_dict[key].lower())
            return list(set(base_ingr))

        self.df["base_ingredients"] = self.df.apply(
            lambda row: extract_base_ingr(row["ingredients"]), axis=1
        )

        def conver_to_vegan(ingr_list):
            vegan_list = []
            for i in ingr_list:
                if i in self.non_vegan_ingr:
                    filtered_df = self.df_non_vegan_alter[
                        self.df_non_vegan_alter["BaseIngredient"] == i
                    ]
                    vegan_alternatives = filtered_df["VeganAlternative"]
                    result_list = [
                        item.strip()
                        for sublist in vegan_alternatives.str.split(",")
                        for item in sublist
                    ]
                    vegan_list.append(result_list[0])
                else:
                    vegan_list.append(i)
            return vegan_list

        # self.df["vegan_ingredients"] = self.df["base_ingredients"].apply(
        #     conver_to_vegan
        # )

        def base_instructions(instructions, ingredients_list):
            if not instructions:  # Check if instructions is None or empty
                return instructions

            for ingr in ingredients_list:
                if ingr is None:  # Skip None values
                    continue
                ingr = ingr.lower()
                found = False
                for key in self.mapping_dict:
                    if found:
                        break
                    if key.lower() in ingr:
                        found = True
                        instructions = instructions.replace(
                            key.lower(), self.mapping_dict[key].lower()
                        )

            return instructions

        self.df["instructions"] = self.df.apply(
            lambda row: base_instructions(row["instructions"], row["ingredients"]),
            axis=1,
        )

    def recommend_recipes(self, user_ingrs):
        def get_user_nonvegan(user_ingrs_temp):
            user_vegan_altr = []
            for i in range(0, len(user_ingrs_temp)):
                ingr = user_ingrs_temp[i].lower()
                if ingr in self.non_vegan_ingr:
                    filtered_df = self.df_non_vegan_alter[
                        self.df_non_vegan_alter["BaseIngredient"] == ingr
                    ]
                    vegan_alternatives = filtered_df["VeganAlternative"]
                    result_list = [
                        item.strip()
                        for sublist in vegan_alternatives.str.split(",")
                        for item in sublist
                    ]
                    user_vegan_altr = user_vegan_altr + result_list
                else:
                    user_vegan_altr.append(ingr)
            return user_vegan_altr

        def vegan_with_available(ingr_list, user_ingrs):
            vegan_list = []
            for i in ingr_list:
                if i in self.non_vegan_ingr:
                    filtered_df = self.df_non_vegan_alter[
                        self.df_non_vegan_alter["BaseIngredient"] == i
                    ]
                    vegan_alternatives = filtered_df["VeganAlternative"]
                    result_list = [
                        item.strip()
                        for sublist in vegan_alternatives.str.split(",")
                        for item in sublist
                    ]

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
            return vegan_list

        def generate_tags(self, base_ingredients, vegan_ingredients):
            combined_list = base_ingredients + vegan_ingredients
            return ", ".join(combined_list)

        def check_ingredients(recipe_ingredients, user_ingredients):
            return len(set(recipe_ingredients).intersection(user_ingredients)) >= 3

        def instructions_with_vegan_available(instructions, ingr_list, user_ingrs):
            for i in ingr_list:
                if i in self.non_vegan_ingr:
                    filtered_df = self.df_non_vegan_alter[
                        self.df_non_vegan_alter["BaseIngredient"] == i
                    ]
                    vegan_alternatives = filtered_df["VeganAlternative"]
                    result_list = [
                        item.strip()
                        for sublist in vegan_alternatives.str.split(",")
                        for item in sublist
                    ]
                    found = False
                    for alter in result_list:
                        if alter in user_ingrs:
                            instructions = instructions.replace(i, alter)
                            found = True
                            break
                    if not found:
                        instructions = instructions.replace(i, result_list[0])

            instructions = ast.literal_eval(instructions)
            return instructions

        # self.df["tags"] = self.df["base_ingredients"].apply(
        #     lambda x: generate_tags(x)
        # )
        def instructions_mod_list(instructions_list):
            instructions_list = ast.literal_eval(instructions_list)
            return instructions_list

        self.df["vegan_ingredients"] = self.df["base_ingredients"].apply(
            lambda x: vegan_with_available(x, user_ingrs)
        )
        self.df["tags"] = self.df.apply(
            lambda row: generate_tags(
                row["base_ingredients"], row["vegan_ingredients"], user_ingrs
            ),
            axis=1,
        )

        self.df["HasEnoughIngredients"] = self.df["vegan_ingredients"].apply(
            lambda x: check_ingredients(x, user_ingrs)
        )
        self.df["vegan_instructions"] = self.df.apply(
            lambda row: instructions_with_vegan_available(
                row["instructions"], row["base_ingredients"], user_ingrs
            ),
            axis=1,
        )

        self.df['instructions'] = self.df['instructions'].apply(instructions_mod_list)

        print(self.df.info())
        # self.df = self.df[self.df["HasEnoughIngredients"]]
        # print(self.df.info())
        user_ingrs = get_user_nonvegan(user_ingrs)
        print("user ingrs = ", user_ingrs)

        # Debugging: print the contents of 'tags'
        print(f"Tags in suitable recipes:\n{self.df['tags'].head()}")

        vectorizer = CountVectorizer(tokenizer=lambda x: x.split(", "))
        X = vectorizer.fit_transform(self.df["tags"])

        # Debugging: print vocabulary size
        print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")

        user_vector = vectorizer.transform([", ".join(user_ingrs)])
        similarities = cosine_similarity(user_vector, X).flatten()

        self.df["Similarity"] = similarities
        recommended_recipes = self.df.sort_values(by="Similarity", ascending=False)
        print(recommended_recipes.info())
        return recommended_recipes
