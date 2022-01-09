import pandas as pd # type: ignore

from random import randint, choices, choice
from typing import Any, Sequence, Annotated, Union, Dict

from data.people.population import gender_enum
from data.people import population as pop
from common_functions import custom_draws, custom_exceptions, extra_funcs
class People:
    """class to generate a dataset

    Returns:
        [type]: [description]
    """
    path_dict = {
        "f_fname": r"data/people/first_name_female_living_10k.csv",
        "f_lname": r'data/people/last_name_female_living_2020_10k.csv',
        "m_fname": r"data/people/first_name_male_living_10k.csv",
        "m_lname": r"data/people/last_name_male_living_10k.csv",
        "age"    : r"data/people/age_data.json"
    }

    @classmethod
    def generate_dataset(cls,
                         rows: Union[int,None] = 1,
                         gender:Union[dict,None] = None,
                         age:Union[dict,None] = None,
                         first_name:Union[dict,None] = None,
                         last_name:Union[dict,None] = None) -> Dict[str, pd.Series[Any]]:

        # load all datasets using in generate people dataset
        f_fname_df = pd.read_csv(cls.path_dict['f_fname']) # female first name
        f_lname_df = pd.read_csv(cls.path_dict["f_lname"]) # female last name
        
        m_fname_df = pd.read_csv(cls.path_dict["m_fname"]) # male first name
        m_lname_df = pd.read_csv(cls.path_dict["m_lname"]) # male last name
        
        age_data_dict = pd.read_json(cls.path_dict['age'])
        
        result = {}
        
        if gender:
            result["gender"] = pd.Series([cls.generate_gender(equal_weight=gender["equal_weight"])
                                          for _ in range(rows)]) #type: ignore
        if age:
            if gender is None or age["equal_weight"]:
                result["age"] = pd.Series([cls.generate_age(age["low_lim"], age["up_lim"], equal_weight=True)
                                        for _ in range(rows)])  #type: ignore
            elif not age["equal_weight"] and gender is not None:
                result["age"] = result["gender"].apply(lambda x: 
                    cls.generate_age(age["low_lim"],age["up_lim"],age_data_dict[x+"s"].to_list()))
                
        if first_name:
            # when gender is unknown
            if gender is not None:
                concan_fname_df = pd.concat([m_fname_df, f_fname_df])
                
                if first_name["double_name_chance"]==0:
                    result["first_name"] = pd.Series([cls.generate_name(concan_fname_df,equal_weight=first_name["equal_weight"])
                                                      for _ in range (rows)]) #type: ignore
            
                elif first_name["double_name_chance"]==100:
                    result["first_name"] = pd.Series([cls.generate_name(concan_fname_df, 2)
                                                      for _ in range (rows)]) #type: ignore
            
                else: 
                    result["first_name"] = pd.Series([cls.generate_name(concan_fname_df,
                                                                        extra_funcs.fast_choices([1,2],
                                                                                     first_name["double_name_chance"]))
                                                      for _ in range (rows)]) #type: ignore
            # when gender is known
            else:
                # and only 1 name
                if first_name["double_name_chance"]==0:
                    result["first_name"] = result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_fname_df if x=="female" else m_fname_df,
                                                                    equal_weight=first_name["equal_weight"]))
                # and only 2 name
                elif first_name["double_name_chance"]==100:
                    result["first_name"] = result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_fname_df if x=="female" else m_fname_df,
                                                                    number_of_names=2,
                                                                    equal_weight=first_name["equal_weight"]))
                # and second name is not sure (0<x<100%)
                else: 
                    result["first_name"] == result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_fname_df if x=="female" else m_fname_df, 
                                                                    extra_funcs.fast_choices([1,2],first_name["double_name_chance"]),
                                                                    equal_weight=first_name["equal_weight"]))
        if last_name:
            # when gender is unknown
            if gender is not None:
                concan_lname_df = pd.concat([m_lname_df, f_lname_df])
                # and everyone has 1 name
                if last_name["double_name_chance"]==0:
                    result["last_name"] = pd.Series([cls.generate_name(concan_lname_df,equal_weight=last_name["equal_weight"])
                                                      for _ in range (rows)]) #type: ignore
                # and everyone has 2 names
                elif last_name["double_name_chance"]==100:
                    result["last_name"] = pd.Series([cls.generate_name(concan_lname_df, 2)
                                                      for _ in range (rows)]) #type: ignore
                # and everyone has 1 or 2 names
                else: 
                    result["last_name"] = pd.Series([cls.generate_name(concan_lname_df,
                                                                        extra_funcs.fast_choices([1,2],
                                                                                     last_name["double_name_chance"]))
                                                      for _ in range (rows)]) #type: ignore
            # when gender is known
            else:
                # and only 1 second name
                if last_name["double_name_chance"]==0:
                    result["last_name"] = result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_lname_df if x=="female" else m_lname_df,
                                                                    equal_weight=last_name["equal_weight"]))
                # and everyone has 2 second names
                elif last_name["double_name_chance"]==100:
                    result["last_name"] = result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_lname_df if x=="female" else m_lname_df,
                                                                    number_of_names=2,
                                                                    equal_weight=last_name["equal_weight"]))
                # and everyone has 1 or 2 second names
                else: 
                    result["last_name"] == result["gender"].apply(lambda x:
                                                                    cls.generate_name(f_lname_df if x=="female" else m_lname_df, 
                                                                    extra_funcs.fast_choices([1,2],last_name["double_name_chance"]),
                                                                    equal_weight=last_name["equal_weight"]))
        

        # result["height"] +=
        # result["weight"] +=

        return result

    @staticmethod
    def generate_age(low_lim:int=0,
                    up_lim:int=100,
                    population:Sequence[int] = None,
                    equal_weight:bool = False)->int:
        """Return age based on population and gender statistics in Poland.

        Args:
            `age_low_lim` (int, optional): Lowest limit of returned value. Defaults to 0|Min.
            `age_up_lim` (int, optional): Upper limit of returned value. Defaults to 100|Max.
            `age_population` (Sequence[int], optional): At n-th index population of n-age. 
                            Higher population -> higher chance to draw. Defaults to None.
            `equal_weight` (bool, optional): Population and gender has no effect on result.
                                        Every value has the same chance. Defaults to False.

        Returns:
            int: Age.
        """
        
        if equal_weight:
            return randint(low_lim, up_lim)
        
        return choices(range(low_lim, up_lim+1), population)[0]
        

    @ staticmethod
    def generate_gender(gender: Sequence[Any] = tuple(gen for gen in gender_enum),
                        chance: Sequence[float] = (pop.gender_chance_enum.FEMALE.value,
                                              pop.gender_chance_enum.MALE.value),
                        equal_weight:bool = False) -> Union[str, Any]:
        """Draws gender of people base on statistics from Poland. 
        Default chance is about 51% for female and 49% for male. 

        Args:
            `symbols` (Sequence[Any], optional): representation of each sex. Defaults to ('female', 'male').
            `chance` (Sequence[float]: chance to draw every option. Defaults to (population_enum.SEX_FEMALE.value, population_enum.SEX_MALE.value).
            `equal_weight` (bool, optional): is True, then every gender has the same chance of being drawn.
        Returns:
            str|Any: Default returned type is string, but you can change it by overriding
            gender arg with other sequence object.
        """
        
        if equal_weight:
            return choice(gender)
        
        if len(gender)!=len(chance):
            raise custom_exceptions.IncorrectLen("""`gender` and `chance` sequences must have the same length. \n
                                                 Exception is if `equal_weight`=`True`""")
        
        return choices(gender, chance)[0]

    @ staticmethod
    def generate_name(name_data: pd.DataFrame,
                      number_of_names: int = 1,
                      equal_weight:bool = False,
                      separator: Annotated[str, 1] = " ") -> str:
        """Return 1 or more names concatenated in 1 string.
        Names are readed from `name_data` df and every of these has population
        (higher population-> higher chance to draw).

        Args:
            name_data (pd.DataFrame): DF[[name:str|Any, population:number]]
            number_of_names (int, optional): Number concatenated names. Defaults to 1.
            equal_weight (bool, optional): If True - ignore population value, equal chance gor eery name.
                                        Defaults to False.
            separator (Annotated[str, 1], optional): Char which will be separate names in column.
                                        Defaults to " ".

        Returns:
            str: Concatenated names into single string.
        """
        return extra_funcs.concatenate_strings(
                        custom_draws.simple_df_draw(name_data, k=number_of_names, equal_weight=equal_weight)
                        ,sep=separator)
    