available_fields = [
# PEOPLE
{
    "name": "gender",
    "description": "Gender. \n Chance for male ~ 49%, for female ~51% (base on population statistics in Poland). \n type: string/text",
    "options":[
        {
            "name": "equal_weight",
            "description": "Equal chance for every gender",
            "input_type": "checkbox",
            "return_type": "bool"
        }
    ]
},
{
    "name": "first_name",
    "description": "Polish first names fit to gender. \n type: string/text",
    "options":[
        {
            "name": "double_name_chance",
            "description": "Chance to double last name in percent.",
            "input_type": "slider",
            "default": 0,
            "max":100,
            "min":0,
            "step":1
        },
        {"name": "equal_weight",
        "description":"Independent of sex of person.",
        "input_type":"checkbox",
        "return_type":"bool"
        }
    ]
},
{
    "name": "last_name",
    "description": "Polish last names fit to gender. \n type: string/text",
    "options":[
        {
            "name": "double_lname_chance",
            "description": "Chance to double last name in percent.",
            "input_type": "slider",
            "default": 0,
            "max":100,
            "min":0,
            "step":1
        },
        {"name": "equal_weight",
        "description":"Independent of sex of person.",
        "input_type":"checkbox",
        "return_type":"bool"
        }
    ]
},
{
    "name": "age",
    "description": "Age of person. Depends on sex.",
    "options":[
        {"name": "equal_weight",
        "description":"Independent of sex of person.",
        "input_type":"checkbox",
        "return_type":"bool"
        },
        {
            "name":"low_lim",
            "description":"Value which means lowest limit of age value. It depends on other fields.",
            "input_type": "number",
            "default":0,
            "max":"up_lim",
            "min":0
        },
        {
            "name":"up_lim",
            "description":"Value which means upper limit of age value. It depends on other fields.",
            "input_type": "number",
            "default":100,
            "max":100,
            "min":"low_lim"
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
            "name": "equal_weight",
            "description": "Postcode no depends on voivodeship. Drawn randomly.",
            "input_type": "checkbox",
            "return_type": "bool"
        }
    ]
}]