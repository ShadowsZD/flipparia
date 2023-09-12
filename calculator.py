import requests
import pandas as pd

class Calculator():
    def __init__(self):

        self.base_item_url = "https://poe.ninja/api/data/itemoverview?league={self.league}&type={item}"
        self.base_currency_url = "https://poe.ninja/api/data/currencyoverview?league={self.league}&type={item}"
        self.league = "Ancestor"

        self.currency_df = self.get_currency_data()
        self.item_df = self.get_item_data()

        self.harvest_df = self.currency_df.filter(like='Lifeforce', axis=0)
        self.delirium_df = self.item_df.filter(like='Delirium Orb', axis=0)
        self.scarab_df = self.item_df.filter(like='Scarab', axis=0)
        self.essence_df = self.item_df.filter(like='Essence', axis=0)

        self.primal_lifeforce_unit_price = self.harvest_df.at["Primal Crystallised Lifeforce", 'chaosValue']
        self.vivid_lifeforce_unit_price = self.harvest_df.at["Vivid Crystallised Lifeforce", 'chaosValue']
        self.wild_lifeforce_unit_price = self.harvest_df.at["Wild Crystallised Lifeforce", 'chaosValue']

    def template_replace(self, template_input, item_type):
        '''
        Replace template url to be an f-string
        '''
        item = item_type
        return eval(f"f'{template_input}'")
    
    def chance_calculator(self, prob_occurence):
        fail_prob = 1 - prob_occurence
        tot_chance = fail_prob
        times = 1
        while tot_chance >= prob_occurence:
            tot_chance = fail_prob ** times
            times += 1
        return times
    
    def get_currency_data(self):
        currencies = ["Currency"]
        currency_price_data = {}
        raw_currency_data = {}

        for currency in currencies:
            raw_currency_data[currency] = requests.get(self.template_replace(self.base_currency_url, currency)).json()
            
        for currency in raw_currency_data["Currency"]["lines"]:
            currency_price_data[currency["currencyTypeName"]] = {
            "chaosValue": currency["chaosEquivalent"]
            }
        
        return pd.DataFrame.from_dict(currency_price_data, orient="index")
    
    def get_item_data(self):
        items = ["Scarab", "DeliriumOrb", "Essence"]
        item_price_data = {}
        raw_item_data = {}

        for item in items:
            raw_item_data[item] = requests.get(self.template_replace(self.base_item_url, item)).json()
        
        for category, data in raw_item_data.items():
            for item in data.get("lines"):
                item_price_data[item["name"]] = {
                    "chaosValue": item["chaosValue"],
                    "exaltedValue": item["exaltedValue"],
                    "divineValue": item["divineValue"]
                }

        return pd.DataFrame.from_dict(item_price_data, orient="index")
    
    def fixed_weight_profit_calc(self, item_df, item_tiers, stack_size, min_profit_margin, craft_cost):

        profit_info = {}

        for tier in item_tiers:
            calc_df = item_df.filter(like=tier, axis=0)
            
            min_value_item = calc_df["chaosValue"].min()
            
            base_cost_item = min_value_item * stack_size
            craft_try_cost = craft_cost * stack_size
            min_craft_cost = min_value_item * stack_size + craft_try_cost
            
            profit_items = calc_df[calc_df["chaosValue"] * stack_size >= min_craft_cost + min_profit_margin]
            
            if len(profit_items) == 0:
                print(f"No profit on {tier} items :(")
            else:
                for i in range(len(profit_items), 0, -1):
                    
                    chance_to_hit = len(profit_items.head(i)) / (len(calc_df) - 1)
                    worst_case_tries = self.chance_calculator(chance_to_hit)

                    best_scenario = base_cost_item + craft_try_cost * 1
                    avg_scenario = base_cost_item + craft_try_cost * (1 / chance_to_hit)
                    worst_scenario = base_cost_item + craft_try_cost * worst_case_tries
                    
                    scenarios = {
                        "Best Scenario": {
                            "cost": best_scenario,
                            "tries": 1
                        },
                        "Avg Scenario": {
                            "cost": avg_scenario,
                            "tries": 1 / chance_to_hit
                        }, 
                        "Worst Scenario": {
                            "cost": worst_scenario,
                            "tries": worst_case_tries
                        }
                    }
                    
                    avg_profit = profit_items.head(i)["chaosValue"].sum() * 10 / len(profit_items.head(i))

                    profit_items_str = ', '.join([str(elem) for elem in profit_items.head(i).index.tolist()])
                    profit_info[profit_items_str] = []

                    print(f"Calculating profit when targetting {profit_items_str}")

                    for scenario, info in scenarios.items():
                        cost = info["cost"]
                        tries = info["tries"]

                        profit = avg_profit - cost

                        profit_info[profit_items_str].append(f"""{scenario} cost: {cost:.0f} C.
                                        Base item: {min_value_item} C x {stack_size} = {min_value_item * stack_size} C.
                                        Crafting try: {craft_try_cost} C x {tries:.0f} = {craft_try_cost * tries:.0f} C.
                                        Profit: {int(profit)} C!""")
        return profit_info
                    
    def delirium_profit_calc(self):
        return self.fixed_weight_profit_calc(self.delirium_df, ["Delirium Orb"], 10, 20, 30 * self.primal_lifeforce_unit_price)

    def scarab_profit_calc(self):
        return self.fixed_weight_profit_calc(self.scarab_df, ["Rusted", "Polished", "Gilded", "Winged"], 10, 20, 30 * self.wild_lifeforce_unit_price)

    def essence_profit_calc(self):
        return self.fixed_weight_profit_calc(self.essence_df, ["Whispering", "Muttering", "Weeping", "Wailing", "Screaming", "Shrieking", "Deafening"], 9, 20, 30 * self.primal_lifeforce_unit_price)

    def profit_calc(self, item_class):
        if(item_class == "Delirium Orbs"):
            return self.delirium_profit_calc()
        if(item_class == "Scarabs"):
            return self.scarab_profit_calc()
        if(item_class == "Essences"):
           return self.essence_profit_calc()

    def refresh_prices(self):
        self.currency_df = self.get_currency_data()
        self.item_df = self.get_item_data()

        self.harvest_df = self.currency_df.filter(like='Lifeforce', axis=0)
        self.delirium_df = self.item_df.filter(like='Delirium Orb', axis=0)
        self.scarab_df = self.item_df.filter(like='Scarab', axis=0)
        self.essence_df = self.item_df.filter(like='Essence', axis=0)

        self.primal_lifeforce_unit_price = self.harvest_df.at["Primal Crystallised Lifeforce", 'chaosValue']
        self.vivid_lifeforce_unit_price = self.harvest_df.at["Vivid Crystallised Lifeforce", 'chaosValue']
        self.wild_lifeforce_unit_price = self.harvest_df.at["Wild Crystallised Lifeforce", 'chaosValue']

if __name__ == '__main__':
    profit_calc = Calculator()