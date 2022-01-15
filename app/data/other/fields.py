from data.other.predefined_types import PredefinedTypes as PT

available_fields = [
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
                        "Dolna granica.",
                        "Wiek będzie równy bądź wyższy od tej wartości."),
            PT.dict_range("up_lim",
                        "Górna granica.",
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
                        "Szansa na podwójne imię.",
                        "Szansa w \% na podwójne imię."),
            PT.dict_checkbox("equal_weight",
                            "Równe wagi.",
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
                        "Szansa na podwójne Nazwisko.",
                        "Szansa w \% na podwójne imię."),
            PT.dict_checkbox("equal_weight",
                            "Równe wagi.",
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
                            "Równe wagi.",
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
                                "Kody nie są dopasowane do województwa."),
                PT.blanck_chance()
            
        ]
    }
]
return_params = [
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

def request_checker(request:dict, available_fields:list = available_fields):
    
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
    