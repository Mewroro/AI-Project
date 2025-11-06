import json
import random

class QuestionBase:
    def __init__(self, category: str):
        self.category = category
        with open("Templates.json", "r") as file:
            self.templates = [template for template in json.load(file) if template["category"] == category]

    def get_random_template(self):
        index = random.randint(0, len(self.templates) - 1)
        return self.templates[index];

    def generate(self):
        pass