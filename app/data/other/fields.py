from typing import Sequence, Dict, Any
from data.other.predefined_types import PredefinedTypes as PT

AVAILABLE_FIELDS = [
    {
        "name": "id",
        "repr": "Id",
        "description":"Unikatowy numer wiersza.",
        "custom_col_name":PT.custom_col_name(),
        "options":[]
    },
     {
        "name":"gender",
        "repr": "Płeć",
        "description": r"""Płeć przedstawiona w postaci ciągu znaków jako 'female', 'male'.
        ~51% szans na kobietę i ~49% szans na kobietę. Szanse na wylosowanie na bazie statystyk z Polski.""",
        "custom_col_name":PT.custom_col_name(),
        "options":[
            PT.dict_checkbox("equal_weight",
                            "Równe szanse",
                            r"Każda z płci ma 50% szans na wylosowanie."),
            PT.blanck_chance()
            ]
    },
    {
        "name": "age",
        "repr": "Wiek",
        "description": "Losowany na bazie popularności w Polsce z uwzględnieniem płci.",
        "custom_col_name":PT.custom_col_name(),
        "options":[
            PT.dict_range("low_lim",
                        "Dolna granica",
                        "Wiek będzie równy bądź wyższy od tej wartości."),
            PT.dict_range("up_lim",
                        "Górna granica",
                        "Wiek będzie równy bądź niższy od tej wartości.",
                        default=100),
            PT.dict_checkbox("equal_weight",
                            "Równe szanse",
                        r"Płeć i popularność nie wpływają na losowany wiek."),
            PT.blanck_chance()
            ]
    },
    {
        "name":"first_name",
        "repr": "Imię",
        "description": "Imię na bazie imion występujących w Polsce. \n Szansa na dane imię jest równoważna z jego popularnością.",
        "custom_col_name":PT.custom_col_name(),    
        "options":[
            PT.dict_range("double_name_chance",
                        "Szansa na podwójne imię",
                        "Szansa w \% na podwójne imię."),
            PT.dict_checkbox("equal_weight",
                            "Równe wagi",
                            "Każde imię ma równe szanse na wysolowanie, popularność nie ma znaczenia."),
            PT.dict_checkbox("unfit_to_gen",
                            "Niedopasowanie do płci",
                            "Imiona są losowe, nie będą dopasowane do płci."),
            PT.blanck_chance()
            ]
    },
    {
        "name": "last_name",
        "repr": "Nazwisko",
        "description": "Nazwisko na bazie nazwisk występujących w Polsce. \n Szansa na dane nazwisko jest równoważna z jego popularnością.",
        "custom_col_name":PT.custom_col_name(),
        "options":[
            PT.dict_range("double_name_chance",
                        "Szansa na podwójne Nazwisko",
                        "Szansa w \% na podwójne imię."),
            PT.dict_checkbox("equal_weight",
                            "Równe wagi",
                            "Każde nazwisko ma równe szanse na wysolowanie, popularność nie ma znaczenia."),
            PT.dict_checkbox("unfit_to_gen",
                            "Niedopasowanie do płci",
                            "Nazwiska są losowe, nie będą dopasowane do płci."),
            PT.blanck_chance()
            ]
    },
# AREAS
    {
        "name": "voivodeship",
        "repr": "Województwo",
        "description":"Województwo na bazie województw w Polsce.\n Zależne od wieku, płci i populacji.",
        "custom_col_name":PT.custom_col_name(),
        "options":[
            PT.dict_checkbox("equal_weight",
                            "Równe wagi",
                            "Każde województwo ma taką samą szansę. Niezależne od innych parametrów."),
            PT.blanck_chance()
            ]
    },
    {
        "name":"postcode",
        "repr": "Kod pocztowy",
        "description": "Kody pocztowe na bazie kodów w Polsce.\n Kody są dopasowane do województwa.",
        "custom_col_name": PT.custom_col_name(),
        "options":[
            
                PT.dict_checkbox("independently",
                                "Niezależny",
                                "Kody nie są dopasowane do województwa."),
                PT.blanck_chance()
            
        ]
    },
    {
        "name":"sportstatus",
        "repr": "Status sportowca",
        "description": "Status sportowca w rozumieniu Junior, Senior lub brak.",
        "custom_col_name": PT.custom_col_name(),
        "options":[
            
                PT.dict_checkbox("independently",
                                "Niezależny",
                                "Szansa na status losowana jest z przypadkowego województwa."),
                PT.dict_checkbox("without_none",
                                 "Bez pustych wartości",
                                 "Losowane jest tylko między statusem junior i senior."),
                PT.dict_checkbox("equal_weight",
                                 "Równe szanse",
                                 "Każdy status ma równe szanse na wylosowanie. Nadpisuje opcje `Niezależny`."),
                PT.blanck_chance()
        ]
    },
    {
        "name":"sportdiscipline",
        "repr": "Dyscyplina sportowa",
        "description": "Losuje się jedynie wtedy, kiedy istnieje jakiś status sportowca.",
        "custom_col_name": PT.custom_col_name(),
        "options":[
                PT.dict_checkbox("without_none",
                                 "Bez pustych wartości",
                                 "Losowane jest tylko między statusem junior i senior."),
                PT.dict_checkbox("equal_weight",
                    "Równe szanse",
                    "Każdy status ma równe szanse na wylosowanie. Nadpisuje opcje `Niezależny`."),
                PT.blanck_chance()
            
        ]
    },
# EDUCATION
    {
        "name":"languages",
        "repr":"Liczba znanych języków",
        "description": "Liczba znanych języków obcych.\n Uwaga! \n Liczba 3 oznaczana 3 lub więcej.\n Brak wartości pojawia się dla osób do 18 roku życia z powodu braku żetelnych danych.",
        "custom_col_name":PT.custom_col_name(),
        "options":[
            PT.dict_checkbox("equal_weight",
                            "Równe wagi",
                            "Szansa na wartość nie jest uzależniona od statystyki. Każdy z języków ma równą szansę."),
            PT.dict_checkbox("without_none",
                             "Wyklucz brak wartości",
                             "Z możliwych wartości zostanie wyrzucona wartość None/null. Osoby <18 roku życia dostana również swoją wartość."),
            PT.blanck_chance()
            ]
    },
    {
        "name": "edu_level",
        "repr": "Poziom wykształcenia",
        "description": "Poziom wykształcenia na podstawie systemu edukacji w Polsce do roku 2016 (przed reformą szkolnictwa).",
        "custom_col_name": PT.custom_col_name(),
        "options":[
            PT.dict_checkbox("equal_weight",
                            "Równe wagi",
                            "Szansa na wartość nie jest uzależniona od statystyki. Każdy stopień wykształcenia ma równą szansę."),
            PT.dict_checkbox("without_none",
                             "Wyklucz brak wartości",
                             "Z możliwych wartości zostanie wyrzucona wartość None/null. Osoby <18 roku życia dostana również swoją wartość."),
            PT.blanck_chance()
                    ]
    },
    {
        "name": "random",
        "repr": "Losowe pole",
        "description": "Wybiera losowe pole z póli niewybranych pól i przydziela mu domyślne parametry.",
        "custom_col_name": PT.custom_col_name(),
        "options":[
            PT.dict_checkbox("random_params",
                            "Losuj parametry",
                            "Losuje parametry dla tego pola."),
            PT.blanck_chance()
                    ]
    }

]
RETURN_PARAMS = [
    PT.dict_number("rows",
                   "Wiersze",
                   "Ilość wygenerowanych wierszy.",
                   1,None,1),
    PT.dict_select("returned_type",
                   "Zwracany typ",
                   "Sposób, w jaki dane zostaną zwrócone.",
                   "json",
                   [
                       PT.dict_option("API JSON", "json"),
                       PT.dict_option("plik CSV", "csv_file"),
                       PT.dict_option("plik JSON", "json_file"),
                       PT.dict_option("tabela HTML", "html_table")
                   ]
                   )
]

# dict of dependencies for better optimalization
DEPENDENCIES = {
    "age":{"equal_weight": "gender"},
    "first_name":{"unfit_to_gen": "gender"},
    "last_name":{"unfit_to_gen": "gender"},
    "voivodeship":{"equal_weight":{"gender", "age"}},
    "postcode":{"independently":"voivodeship"},
    "sportstatus":{"random_chance":{"age","voivodeship"}},
    "sportdiscipline":{"independently":{"sportstatus", "voivodeship"}},
    "languages":{"equal_weight":{"gender","age"}},
    "edu_level":{"equal_weight":{"gender", "languages"}}
}

def check_dependencies(requested_fields:Dict[str, str]
                       ,dependencies:Dict[str,Dict[str,str]] = DEPENDENCIES
                       )-> Sequence[Any]:
    required_columns = set(requested_fields.keys())
    
    # for every requested field
    for rf, param_dict in requested_fields.items():
        if rf in set(dependencies.keys()):
            # if condition to be independence hasn't been met
            for required_to_independence in dependencies[rf]:
                if not param_dict.get(required_to_independence):
                    # add field to required set
                    if isinstance(required_param:=dependencies[rf][required_to_independence], str):
                        required_columns.add(required_param)
                    else:
                        required_columns = required_columns.union(required_param)
                    
    return required_columns
            

def request_checker(request:Dict[str,Any], available_fields:list = AVAILABLE_FIELDS):
    
    # get default parameters for fields
    field_params = get_default_params(available_fields)
    
    # get list of requested parameters
    request_fields = set(request.keys())
    
    for field in field_params:
        if field in request_fields:
            # if field is requested -> overwrite it
            field_params[field] = request[field]
    
    # return default params overwrite by user request
    return field_params
            
            

def get_default_params(available_fields)->dict:
    """Convert `available_fields` list to 
    expected requests data form to compare it to request data.

    Args:
        available_fields ([type]): [description]

    Returns:
        dict: [description]
    """
    return { field_dict["name"]:{ option["name"]:option["default"]
            for option in field_dict["options"]}
         for field_dict in available_fields }