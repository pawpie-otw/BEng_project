from common_functions.custom_draws import draw_from_df
from data.athletes.sports_data import Data

import pandas as pd


class Athletes:

    '''Class for generating athletes dataset'''

    data = Data()

    @classmethod
    def create_provinces_dict(cls):
        all_sports = cls.data.join_all_sports()
        all_to_dict = all_sports.drop(columns=["Nazwa"])
        sport_names = []
        for col in all_to_dict.columns:
            sport_names.append(col)
        sport_names_series = pd.Series(sport_names)
        dfs_provinces_dict = {}
        for index, row in all_sports.iterrows():
            dfs_provinces_dict[row[0]] = pd.DataFrame(
                {'Name': sport_names_series, 'People': row[1:].reset_index(drop=True)})

        return dfs_provinces_dict

    @staticmethod
    def generate_dataset(df: pd.DataFrame) -> pd.Series:

        return pd.Series([draw_from_df(__class__.create_provinces_dict()[voivodship])
                          for voivodship in df.voivodship])

    @staticmethod
    def sport_status_chance(voivodeship: str, age: int, df: pd.DataFrame) -> float:
        """Return chance as float number to become a sportman in given voivodeship.
        Every voivodeship has diffrent total population and population involved in sports in diffrent age.

        Args:
            voivodeship (str): voivodeship 
            age (int): 
            df (pd.DataFrame): df contains chance to become a junior or senior in sport experience meaning.

        Returns:
            chance: chance to become a sportman in given voivodeship in given age.
        """
        if 15 > age or age > 45:
            return 0

        elif 39 < age < 46:
            return df.loc[voivodeship, "senior_chance"]/2

        elif 18 > age > 14:
            return df.loc[voivodeship, "junior_chance"]
        return df.loc[voivodeship, "senior_chance"]
