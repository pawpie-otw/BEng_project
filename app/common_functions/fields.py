available_fields = [
# PEOPLE
{
    "name": "gender",
    "description": "Gender. \n Chance for male ~ 49%, for female ~51% (base on population statistics in Poland). \n type: string/text",
    "options":[
        {
            "name": "Equal",
            "description": "Equal chance for every gender",
            "input_type": "checkbox",
            "return_type": "bool"
        }
    ]
},
{
    "name": "first name",
    "description": "Polish first names fit to gender. \n type: string/text",
    "options":[
        {
            "name": "num_of_fnames",
            "description": "Number of first names",
            "input_type": "select",
            "default": 1,
            "options": [1,2,3],
            "return_type": "int",
            "dependecy":{
                "field":"unregular_num_of_fnames",
                1: "blocked",
                2: "unblocked",
                3: "unblocked"
                }
        },
        {
            "name": "unregular_num_of_fnames",
            "description": "Unregular number of first names",
            "input_type": "checkbox",
            "return_type": "bool",
        }
    ]
},
{
    "name": "last name",
    "description": "Polish last names fit to gender. \n type: string/text",
    "options":[
        {
            "name": "num_of_fnames",
            "description": "Number of last names",
            "input_type": "select",
            "default": 1,
            "options": [1,2],
            "return_type": "int",
            "dependecy":{
                "field":"double_lname_chance",
                1: "blocked",
                2: "unblocked"
                }
        },
        {
            "name": "double_lname_chance",
            "description": "Chance to double last name in percent.",
            "input_type": "number",
            "default": 15,
            "max":100,
            "min":0
        }
    ]
},
{
    "name": "age",
    "description": "Age of person. Depends on sex.",
    "options":[
        {"name": "equal_age_chance",
        "description":"Independent of sex of person.",
        "input_type":"checkbox",
        "return_type":"bool"
        },
        {
            "name":"age_low_lim",
            "description":"Value which means lowest limit of age value. It depends on other fields.",
            "input_type": "number",
            "default":0,
            "max":"age_up_lim",
            "min":0
        },
        {
            "name":"age_up_lim",
            "description":"Value which means upper limit of age value. It depends on other fields.",
            "input_type": "number",
            "default":100,
            "max":100,
            "min":"age_low_lim"
        }
    ]
},
# AREAS
{
    "name":"voivodeship",
    "description":"Polish voivodeships, depends on age and population.",
    "options":[
        {
            "name": "equal_weight",
            "description": "Equal chance for every voivodeship. Independent of anythink.",
            "input_type": "checkbox",
            "return_type": "bool"
        }
    ]
},
{
    "name":"postcode",
    "description":"Polish postcodes, depends on voivodeship if it's possible.",
    "options":[
        {
            "name": "no_dependence",
            "description": "Postcode no depends on voivodeship. Drawn randomly.",
            "input_type": "checkbox",
            "return_type": "bool"
        }
    ]
}]