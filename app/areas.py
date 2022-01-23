import pandas as pd # type: ignore

from random import choice,choices
from json import load
from typing import Sequence, Union, Any, Dict



from common_functions import custom_exceptions
from common_functions import loggers
from data.areas.areas_const import VOIVODESHIP

class Areas:
    datafolder_path = r"data/areas"
    path_dict = {
        "voivodeship_males": datafolder_path + r"/voivodeship_males_by_sexage.csv",
        "voivodeship_females": datafolder_path + r"/voivodeship_females_by_sexage.csv",
        "postcodes": datafolder_path + r"/post_codes.json"
    }


    @classmethod
    def generate_dataset(cls, 
                         required_cols:set,
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

        
        
        
        result = pd.DataFrame()

        # VOIVODESHIP
        if "voivodeship" in required_cols:
            result["voivodeship"] = cls.complete_voivodeship(rows, voivodeship, base_df, required_cols)
        
        # POSTCODE
        if "postcode" in required_cols:
            result["postcode"] = cls.complete_postcode(rows, postcode, result, required_cols)
            
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
        
    @classmethod
    @loggers.timeit_and_log("logs/exec_logs.log")
    def complete_postcode(cls, rows, postcode, base_df, required_cols):
        postcode_data = dict(load(open(cls.path_dict["postcodes"], encoding="utf8")))
        if "voivodeship" in required_cols:
            return tuple(cls.generate_postcode(postcode_data,
                                                    voivodeship,
                                                    postcode["independently"])
                            for voivodeship in base_df.voivodeship)
        else:
            return tuple(cls.generate_postcode(postcode_data, independently=True)
                         for _ in range(rows))
    
    @classmethod
    @loggers.timeit_and_log("logs/exec_logs.log")
    def complete_voivodeship(cls, rows, voivodeship, base_df, required_cols):
        
        voivodeship_data = {"males": pd.read_csv(cls.path_dict["voivodeship_males"], index_col="index"),
                    "females": pd.read_csv(cls.path_dict["voivodeship_females"], index_col="index")}
        
        if {"gender","age"}.issubset(required_cols):
            return tuple(cls.generate_voivodeship(voivodeship_data[gender+"s"],
                                                        age,
                                                        equal_weight=voivodeship.get("equal_weight"))
                                for gender, age in zip(base_df.gender, base_df.age))
            
        return tuple(cls.generate_voivodeship(equal_weight=True)
                                for _ in range(rows))


    @staticmethod
    def generate_voivodeship(voivodeship_data: Union[pd.DataFrame,None] = None, 
                             age: Union[None, int] = None,
                             equal_weight: bool = False,
                             voivodeship_list:Sequence[str]=VOIVODESHIP) -> Union[Any, str]:
        """Draw and return name of polish voivodeship based on population (which is equal to weight in drawing) that
        the ``voivodeship_population_dataset`` arg containts.

        Args:
            ``age`` (int): Age of person to whom the result will be matched.
            ``voivodeship_population_dataset`` (pd.DataFrame): df containts population group by age and voivodeship.
            ``equal_weight`` (bool, optional): If true, population doesn't matter - every choice is equal. Defaults to False.

        Returns:
            (str): Name of voivodeship in Poland.
        """

        if equal_weight:
            return choice(voivodeship_list)
        
        
        elif (age is not None) and (voivodeship_data is not None):
            
            # age veryfication, dataset shows up to 85 yo.
            age_:int = 85 if age > 85 else 0 if age < 0 else age
            
            return choices(voivodeship_data.columns,
                           voivodeship_data.iloc[age_].to_list())[0]