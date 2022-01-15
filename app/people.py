import pandas as pd

from json import loads
from random import randint, choices, choice
from typing import Any, Sequence, Annotated, Union

from data.people.population import gender_enum
from data.people import population as pop
from common_functions import custom_draws, custom_exceptions, extra_funcs
class People:
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
                         last_name:Union[dict, None] = None) -> pd.DataFrame:

        # load all datasets using in generate people dataset
        f_fname_df = pd.read_csv(cls.path_dict['f_fname']) # female first name
        f_lname_df = pd.read_csv(cls.path_dict["f_lname"]) # female last name
        
        m_fname_df = pd.read_csv(cls.path_dict["m_fname"]) # male first name
        m_lname_df = pd.read_csv(cls.path_dict["m_lname"]) # male last name
        
        age_data_dict = pd.read_json(cls.path_dict['age'])
        
        result = pd.DataFrame()
        # GENDER
        result["gender"] = [cls.generate_gender(equal_weight=gender.get("equal_weight"))
                                          for _ in range(rows)]
        
        # AGE
        if age.get("equal_weight"):
            result["age"] = [cls.generate_age(age["low_lim"], age["up_lim"], equal_weight=True)
                                        for _ in range(rows)]
        else:
            result["age"] = [cls.generate_age(age["low_lim"], age["up_lim"], age_data_dict[x].to_list())
                             for x in result.gender]
                
        # FIRST NAME
        num_of_fname_gen_res = cls.calc_name_num(first_name["double_name_chance"], rows)
        
        # when gender is unimportant
        if first_name.get("unfit_to_gen"):
            concan_fname_df = pd.concat([m_fname_df, f_fname_df])
            
            result["first_name"] = [cls.generate_name(concan_fname_df, 
                                                      number_of_names=num,
                                                      equal_weight=first_name["equal_weight"]) 
                                    for num in num_of_fname_gen_res]
        else:
            result["first_name"] = [cls.generate_name(f_fname_df if gender=="female" 
                                                      else m_fname_df,
                                                      number_of_names=num,
                                                      equal_weight=first_name["equal_weight"])
                                    for gender, num in zip(result.gender, num_of_fname_gen_res)]
        
        # LAST NAME
        num_of_lname_gen_res = cls.calc_name_num(last_name["double_name_chance"], rows)
        if last_name.get("unfit_to_gen"):
            concan_lname_df = pd.concat([m_lname_df, f_lname_df])
            
            result["last_name"] = [cls.generate_name(concan_lname_df,
                                                     number_of_names=num,
                                                     equal_weight=last_name["equal_weight"])
                                    for num in num_of_lname_gen_res]
        else:
            result["last_name"] = [cls.generate_name(f_lname_df if gender=="female" 
                                                      else m_lname_df,
                                                      number_of_names=num,
                                                      equal_weight=first_name["equal_weight"],
                                                      separator="-")
                                    for gender, num in zip(result.gender, num_of_lname_gen_res)]

        # result["height"] +=
        # result["weight"] +=

        for key in result:
            result[key].name = key
        
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
            return choice(gender).value
        
        if len(gender)!=len(chance):
            raise custom_exceptions.IncorrectLen("""`gender` and `chance` sequences must have the same length. \n
                                                 Exception is if `equal_weight`=`True`""")
        
        return choices(gender, chance)[0].value

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
    @staticmethod
    def calc_name_num(chance:int, rows:int)->int:
        
        if chance ==0:
            return (1 for _ in range(rows))
        elif chance == 100:
            return (2 for _ in range(rows))
        
        return (2 if randint(1,99) <= chance else 1
                for _ in range(rows))

if __name__ == '__main__':
    json_string = """{
    "rows":40,
    "response_format":"typical_json",
    "gender":{
        "equal_weight": true
    },
    "age":{
        "equal_weight":true,
        "low_lim":0,
        "up_lim":100
    },
    "first_name":{
        "double_name_chance":15,
        "equal_weight":false
    },
    "last_name":{
        "double_name_chance":15,
        "equal_weight":false
        }
    }"""

    request_dict = loads(json_string)
    print(request_dict)
    print(request_dict.get("rows"))
    result = People.generate_dataset(rows = request_dict.get("rows"),
                        gender = request_dict.get("gender"),
                        age = request_dict.get("age"),
                        first_name = request_dict.get("first_name"),
                        last_name = request_dict.get("last_name"))
    print(pd.DataFrame(result))