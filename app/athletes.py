from email.mime import base
import pandas as pd

from typing import Union, Dict, Any
from random import choices, choice, randint

from common_functions.extra_funcs import fast_choices
from common_functions import custom_draws
from common_functions import loggers

from data.areas import areas_const

class Athletes:

    '''Class for generating athletes dataset'''

    path_dict = {
        "sportstatus":r"data/athletes/sportstatus_chance.csv",
        "sports_per_voivodship":r"data/athletes/sports_per_voivodship.csv",
        "all_sports":r"data/athletes/all_sports.csv"
    }
    
    

    @classmethod
    def generate_dataset(cls,
                         rows: Union[None,int],
                         required_cols,
                         base_df: Union[None, pd.DataFrame] = None,
                         sportstatus:Union[None, Dict[str, Any]] = None,
                         sportdiscipline:Union[None, Dict[str, Any]] = None) -> Dict[str, pd.Series]:
        
        result = pd.DataFrame()
        
        if "sportstatus" in required_cols:
            result["sportstatus"] = cls.complete_sportstatus(rows,sportstatus, base_df, required_cols)
        
        
        if "sportdiscipline" in required_cols:
            result["sportdiscipline"] = cls.complete_sportdiscipline(
                rows, sportdiscipline, pd.concat([base_df, result], axis=1), required_cols)
        
        return result
    
    @classmethod
    def complete_sportdiscipline(cls, rows, sportdiscipline, base_df, required_cols):
        all_sports = pd.read_csv(cls.path_dict["all_sports"])
        
        if {"voivodeship", "sportstatus"}.issubset(required_cols) \
            and not sportdiscipline["without_none"]:
            
            return tuple(cls.generate_discipline(all_sports, voivodeship, 
                                                 equal_weight=sportdiscipline["equal_weight"])
                         if sportstatus else None
                     for voivodeship, sportstatus in zip(base_df.voivodeship, base_df.sportstatus))
        
        elif "voivodeship" in required_cols and sportdiscipline["without_none"]:
            return tuple(cls.generate_discipline(all_sports, voivodeship, 
                                                 equal_weight=sportdiscipline["equal_weight"])
                     for voivodeship in base_df.voivodeship)
        
        return tuple(cls.complete_sportdiscipline(all_sports, equal_weight=True)
                     for _ in range(rows))
            
    
    @classmethod
    def generate_discipline(cls, sportdiscipline_data:pd.DataFrame,
                            voivodeship=None, equal_weight=False)->str:
        
        if equal_weight or voivodeship is not None:
            return choice(sportdiscipline_data.columns)
        
        return choices(sportdiscipline_data.columns,
                       sportdiscipline_data.loc[voivodeship])
            
    
    @classmethod
    def complete_sportstatus(cls, rows, sportstatus, base_df, required_cols):
        if sportstatus["equal_weight"]:
            return tuple(cls.generate_sportstatus(equal_weight=True,
                                                  without_none=sportstatus["without_none"])
                         for _ in range(rows))
        
        
        sportstatus_data = pd.read_csv(cls.path_dict["sportstatus"], index_col='voivodeship')
        
        if sportstatus["independently"]:
            return tuple(cls.generate_sportstatus(sportstatus_data,
                                                  voivodeship=choice(areas_const.VOIVODESHIP),
                                                  age=randint(0,100))
                     for _ in range(rows))
        elif {"age", "voivodeship"}.issubset(required_cols):
            
            return  tuple(cls.generate_sportstatus(sportstatus_data,
                                                        voivodeship,
                                                        age, without_none=sportstatus["without_none"])
                                for age, voivodeship in zip(base_df.age, base_df.voivodeship))
        
        # if not "voivodeship" in required_cols:
        #     voivodeship_gen = (choice(areas_const.VOIVODESHIP)
        #                        for _ in range(rows))
        # if not "age" in required_cols:
        #     age_gen = (choice(randint(0,100))
        #                        for _ in range(rows))
        
    
    
    
    @classmethod
    def generate_sportstatus(cls,
                        sportchance_data:pd.DataFrame,
                        voivodeship: str = None,
                        age: int = None,
                        equal_weight:bool = False,
                        without_none:bool = False)->pd.DataFrame:
        """Return sportstatus, one of {`None`, `"Junior"`, `"Senior"`}.
        Return depends mainly on sportchance_data, less on `age` and `voivodeship`
        or chance is drawn from `sportchance_data`.

        Args:
            `sportchance_data` (pd.DataFrame): df contains chance to get sportstatus 
                            depends on voivodeship and age.
            `voivodeship` (str, optional): One of `voivodeships` in Poland. 
                                        Required if `independently` = `False`.Defaults to None.
            `age` (int, optional): Age of person. Defaults to None.
            `independently` (bool, optional): If `True`, `age` and `voivodeship` have no effect
                                            to result. Defaults to False.

        Returns:
            Union[str, None]: Return str, if "Junior"|"Senior", else None.
        """
        
        if without_none:
            pool = ["Junior", "Senior"]
        else:
            pool = ["Junior", "Senior", None]
        
        if equal_weight:
            return choice(pool)
            
        # out of accept age range
        elif age < 15 or age > 45:
            return None
        # junior
        elif 18> age>=15:
            return fast_choices(["Junior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age))
        # senior   
        elif age<39:
            return fast_choices(["Senior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age))
        # older senior
        elif age>=40:
            return fast_choices(["Senior", None], 
                                cls.sport_status_chance_by_data(sportchance_data,
                                                                voivodeship,
                                                                age)/2)
    
    @staticmethod
    def sport_status_chance_by_data(df: pd.DataFrame,
                                    voivodeship: str,
                                    age: int) -> float:
        """Return chance as float number to become a sportman in given voivodeship.
        Every voivodeship has diffrent total population and population involved in sports in diffrent age.

        Args:
            voivodeship (str): voivodeship 
            age (int): 
            df (pd.DataFrame): df contains chance to become a junior or senior in sport experience meaning.

        Returns:
            chance: chance to become a sportman in given voivodeship in given age.
        """
        if age < 15 or age > 45:
            return 0.
        elif age > 39 and age < 46:
            return df.at[voivodeship, "senior_chance"]/2
        elif age < 18 and age > 14:
            return df.at[voivodeship, "junior_chance"]
        return df.at[voivodeship, "senior_chance"]