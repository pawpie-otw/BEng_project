import pandas as pd

from typing import Any
from random import choices, choice

from common_functions import extra_funcs
from data.education.education_data import EDU_LEVELS, NUMBER_OF_LANGS
from common_functions import loggers


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
                        "podstawowe": "primary",
                        "bez formalnego wykształcenia": "incomplete primary"}

    path_dict = {
        "female_by_age": r"data\education\female_languages_by_age.xlsx",
        "female_by_edu": r"data\education\female_languages_education.xlsx",
        "male_by_age": r"data\education\male_languages_by_age.xlsx",
        "male_by_edu": r"data\education\male_languages_education.xlsx"}

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
    @loggers.timeit_and_log("logs/exec_logs.log")
    def complete_edu_level(cls,
                           rows,
                           edu_level,
                           required_cols,
                           base_df):

        by_edu_df = {"female": pd.read_excel("data/education/female_languages_education.xlsx"),
                     "male": pd.read_excel("data/education/male_languages_education.xlsx")}

        if edu_level.get("equal_weights", False) or not {"gender", "languages"}.issubset(required_cols):
            return tuple(cls.generate_edu_level(equal_weight=True, map_to_polish=True)
                         for _ in range(rows))

        if {"gender", "languages"}.issubset(required_cols):
            return tuple(cls.generate_edu_level(by_edu_df[gender], number_of_lang, map_to_polish=True)
                         for gender, number_of_lang in zip(base_df.gender, base_df.languages))

    @classmethod
    def generate_edu_level(cls, education_data: pd.DataFrame = None, number_of_langs=None, equal_weight=False, map_to_polish=False) -> str:

        if equal_weight or number_of_langs:
            edu = choice(EDU_LEVELS)

        elif number_of_langs is None:
            edu = "Incomplete primary"
        else:
            column = extra_funcs.find_by_value(cls.number_of_lan_mapper,
                                               number_of_langs)
            edu = choices(EDU_LEVELS,
                          education_data[column].to_list())[0]

        if map_to_polish:
            return extra_funcs.find_by_value(cls.education_mapper,
                                             edu)
        return edu

    @classmethod
    @loggers.timeit_and_log("logs/exec_logs.log")
    def complete_num_of_langs(cls, rows, num_of_langs, required_cols, base_df):

        by_edu_df = {"male": pd.read_excel(cls.path_dict["male_by_edu"], index_col="edu_level"),
                     "female": pd.read_excel(cls.path_dict["female_by_edu"], index_col="edu_level")}

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

        elif age < 18:
            if without_none:
                column = "18 - 24"
            elif age < 18:
                return None
        else:
            print((age-24)//5)
            print(len(language_data.index), language_data.index)
            column = language_data.index[-1] if age >= 69 else language_data.index[
                ((age-24)//5)-1]

        return cls.number_of_lan_mapper[choices(NUMBER_OF_LANGS,
                                                language_data.loc[column].to_list())[0]]
