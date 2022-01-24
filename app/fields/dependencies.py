DEPENDENCIES = {
    "age":{"equal_weight": "gender"},
    "first_name":{"unfit_to_gen": "gender"},
    "last_name":{"unfit_to_gen": "gender"},
    "voivodeship":{"equal_weight":{"gender", "age"}},
    "postcode":{"independently":"voivodeship"},
    "sportstatus":{"random_chance":{"age","voivodeship"}},
    "sportdiscipline":{"equal_weight":{"sportstatus", "voivodeship"}},
    "languages":{"equal_weight":{"gender","age"}},
    "edu_level":{"equal_weight":{"gender", "languages"}}
}