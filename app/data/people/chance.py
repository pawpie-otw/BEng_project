
class Chance:
    def load_by_age(self, age_from: int, age_to: int) -> float:
        
        with open(r"./population.json") as f:
            pop_data = json.load(f)
        
        requested_group_amount = sum([pop_data[group][str(age)]
                                      for age in range(age_low_lim, age_up_lim+1)])
        total_group_amount = sum([pop_data["total"][str(age)]
                                  for age in range(age_low_lim, age_up_lim+1)])
