import pandas as pd
import numpy as np

from typing import Sequence
from random import choices, choice

from common_functions import extra_funcs
from data.education.education_data import EDU_LEVELS, NUMBER_OF_LANGS


class Education:

    number_of_lan_mapper = {
        "no_one": 0,
        "one": 1,
        "two": 2,
        "tree_or_more": 3}

    education_mapper = {"Wyższe": "Tertiary",
                        "Policealne": "Post-secondary",
                        "Średnie zawodowe": "Technical secondary",
                        "Średnie ogólnokształcące": "General secondary",
                        "Zasadnicze zawodowe": "Basic vocational",
                        "Gimnazjalne": "Lower secondary",
                        "podstawowe": "Primary",
                        "bez formalnego wykształcenia": "Incomplete primary"}

    path_dict = {
        "female_by_age": r"data\education\female_languages_by_age.csv",
        "female_by_edu": r"data\education\female_languages_education.csv",
        "male_by_age": r"data\education\male_languages_by_age.csv",
        "male_by_edu": r"data\education\male_languages_education.csv"}

    @classmethod
    def generate_dataset(cls, rows, required_cols, base_df: pd.DataFrame, languages: dict, edu_level: dict
                         ) -> pd.DataFrame:

        result = pd.DataFrame()

        if "languages" in required_cols:
            result["languages"] = cls.complete_num_of_langs(
                rows, languages, required_cols, base_df)

        if "edu_level" in required_cols:
            result["edu_level"] = cls.complete_edu_level(
                rows, edu_level, required_cols, pd.concat([base_df, result], axis=1))

        return result

    @classmethod
    def complete_edu_level(cls,
                           rows,
                           edu_level,
                           required_cols,
                           base_df):

        by_edu_df = {"female": pd.read_csv("data/education/female_languages_education.csv", index_col="edu_level"),
                     "male": pd.read_csv("data/education/male_languages_education.csv", index_col="edu_level")}

        if edu_level.get("equal_weights", False):
            return tuple(cls.generate_edu_level(equal_weight=True, map_to_polish=True, ignore_age=edu_level["ignore_age"])
                         for _ in range(rows))

        if {"gender", "languages", "age"}.issubset(required_cols):
            return tuple(cls.generate_edu_level(by_edu_df[gender],age, number_of_lang, map_to_polish=True, ignore_age=edu_level["ignore_age"])
                         for gender, number_of_lang, age in zip(base_df.gender, base_df.languages, base_df.age))

    @classmethod
    def generate_edu_level(cls, education_data: pd.DataFrame = None, age=None, number_of_langs=None, equal_weight=False, map_to_polish=False, ignore_age=None) -> str:
        
        
        if number_of_langs is None or np.isnan(number_of_langs):    
            column = "no_one"
        else:
            column = cls.map_languages_to_str(cls.number_of_lan_mapper,
                                            number_of_langs)
        
        if ignore_age:
            idx = cls.select_edu_options(age)-2
            edu_lev_list:Sequence[str] = education_data.index[:idx:-1]
            population = education_data[column][:idx:-1]
        else:
            edu_lev_list=education_data.index
            population=education_data[column]
        if equal_weight:
            edu = choice(edu_lev_list)
        else:
            edu = choices(edu_lev_list, population)[0]
        
        if map_to_polish:
            res =  extra_funcs.find_by_value(cls.education_mapper,
                                             edu)
        else:
            res = edu
        return res

    @staticmethod
    def select_edu_options(age):
        
        if age>=21:
            return -7
        if age>=20:
            return -6
        if age>=19:
            return -5
        if age>=18:
            return -4
        elif age>=15:
            return -2
        elif age>=11:
            return -1
        else:
            return 0
        
        
    
    @classmethod
    def complete_num_of_langs(cls, rows, num_of_langs, required_cols, base_df):

        by_edu_df = {"male": pd.read_csv(cls.path_dict["male_by_edu"], index_col="edu_level"),
                     "female": pd.read_csv(cls.path_dict["female_by_edu"], index_col="edu_level")}

        if num_of_langs["equal_weight"] or not {"age", "gender"}.issubset(required_cols):
            return tuple(cls.generate_number_of_langs(equal_weight=True)
                         for _ in range(rows))

        if {"age", "gender"}.issubset(required_cols):
            return tuple(cls.generate_number_of_langs(by_edu_df[gender], age, num_of_langs["equal_weight"],
                                                      without_none=num_of_langs["without_none"])
                         for gender, age in zip(base_df.gender, base_df.age))

    @classmethod
    def generate_number_of_langs(cls,
                                 language_data: pd.DataFrame = None,
                                 age: int = None,
                                 equal_weight: bool = False,
                                 without_none: bool = False) -> int:
        if equal_weight:
            return cls.number_of_lan_mapper[choice(NUMBER_OF_LANGS)]
        elif age<3:
            return 0
        elif age < 18:
            if without_none:
                column = "18 - 24"
            elif age < 18:
                return None
        else:
            column = language_data.index[-1] if age >= 69 else language_data.index[
                ((age-24)//5)-1]

        x= cls.number_of_lan_mapper[choices(NUMBER_OF_LANGS,
                                                language_data.loc[column].to_list())[0]]
        return x
        
    @classmethod
    def map_languages_to_str(cls, dict_, lang_num):
        
        if str(lang_num)=='nan':
            return None
        elif lang_num is None:
            return None
        else:
            return extra_funcs.find_by_value(dict_, lang_num)
