import pandas as pd # type: ignore

from random import choice,choices
from json import load
from typing import Union, Any, Dict

from common_functions import custom_exceptions

class Areas:
    datafolder_path = r"data/areas"
    path_dict = {
        "voivodship_males": datafolder_path + r"/voivodship_males_by_sexage.csv",
        "voivodship_females": datafolder_path + r"/voivodship_females_by_sexage.csv",
        "postcodes": datafolder_path + r"/post_codes.json"
    }


    @classmethod
    def generate_dataset(cls, 
                         rows: Union[None, int] = 1,
                         base_df: Union[None, pd.DataFrame] = None, 
                         voivodeship:Union[None, Dict[str,bool]] = None,
                         postcode:Union[None, Dict[str,bool]] = None)-> dict[str, pd.Series]:
        """Generate data related to administrative areas in Poland - voivodeship and postcode.

        Args:
            `base_df` (pd.DataFrame[['gender'','age']], optional): If given, then possible is to create non-random data, but based on other data. Defaults to None.
            `n` (int, optional): number of requested fields. It's required if base_df is None. Defaults to None.
            `voivodeship_params` (dict, optional): If not None - return column `voivodeships`,
                                                build as {equal_weight:  [bool] val}. Defaults to None.
            `postcode_params` (dict, optional): If not None - return column `postcode`,
                                                build as {equal_weight:  [bool] val}. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame with columns you choosen (by givin the params).
        """

        voivodship_data = {"males": pd.read_csv(cls.path_dict["voivodship_males"]),
                    "females": pd.read_csv(cls.path_dict["voivodship_females"])}
        postcode_data = dict(load(open(cls.path_dict["postcodes"], encoding="utf8")))
        
        result = pd.DataFrame()

        # VOIVODESHIP
        result["voivodeship"] = [cls.generate_voivodeship(voivodship_data[gender+"s"],
                                                        age,
                                                        equal_weight=voivodeship.get("equal_weight"))
                                for gender, age in zip(base_df.gender, base_df.age)]
        
        # POSTCODE
        result["postcode"] = [cls.generate_postcode(postcode_data,
                                                    voivodeship,
                                                    independently=postcode.get("independently"))
                            for voivodeship in result.voivodeship]
        return result

    @staticmethod
    def generate_postcode(dataset:dict,
                          voivodeship:str=None,
                          independently:bool=False)->str:
        """Return postcode which depends on  given voivodeship (if `age` not None)
        or randomly (if `independently=True`).

        Args:
            dataset (dict): dict build as {voivodeship_name:[postcode0,postcode1 ...],}
            voivodeship (str, optional): the value (voivodeship name) on which the result depends. 
            independently (bool, optional): if True, then no needed `age` value - result is drawn randomly.

        Returns:
            str: polish post-code
        """
        if independently:
            return choice(dataset[choice(tuple(dataset.keys()))])
        
        
        try:
            return choice(dataset[voivodeship])
        except Exception as e:
            print("bladdd")
            print(dataset.keys())
            print(voivodeship)
            return "an error place"
        

    @staticmethod
    def generate_voivodeship(voivodeship_data: Union[pd.DataFrame,None] = None, 
                             age: Union[None, int] = None,
                             equal_weight: bool = False) -> Union[Any, str]:
        """Draw and return name of polish voivodship based on population (which is equal to weight in drawing) that
        the ``voivodeship_population_dataset`` arg containts.

        Args:
            ``age`` (int): Age of person to whom the result will be matched.
            ``voivodeship_population_dataset`` (pd.DataFrame): df containts population group by age and voivodship.
            ``equal_weight`` (bool, optional): If true, population doesn't matter - every choice is equal. Defaults to False.

        Returns:
            (str): Name of voivodship in Poland.
        """
        voivodships = ['DOLNOŚLĄSKIE', 'KUJAWSKO-POMORSKIE', 'LUBELSKIE', 'LUBUSKIE',
                       'ŁÓDZKIE', 'MAŁOPOLSKIE', 'MAZOWIECKIE', 'OPOLSKIE', 'PODKARPACKIE',
                       'PODLASKIE', 'POMORSKIE', 'ŚLĄSKIE', 'ŚWIĘTOKRZYSKIE',
                       'WARMIŃSKO-MAZURSKIE', 'WIELKOPOLSKIE', 'ZACHODNIOPOMORSKIE']

        if equal_weight:
            return choice(voivodships)
        
        
        elif (age is not None) and (voivodeship_data is not None):
            
            # age veryfication, dataset shows up to 85 yo.
            age_:int = 85 if age > 85 else 0 if age < 0 else age
            
            return choices(voivodeship_data.columns,
                           voivodeship_data.iloc[age_].to_list())[0]