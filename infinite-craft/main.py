import os


from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "You are a crafting machine. When given two ingredients, you craft them into a new crafting ingredient. As an example, if you are given Water and Wind, you would craft Wave. You respond with single answer response, with no punctuation, as if you were a machine spitting out a newly crafted ingredient.\n\nYou are given {first} and {second}. What do you craft?"
)

model = ChatOpenAI(model="gpt-4-1106-preview")
chain = prompt | model

# print(chain.invoke({"first": "Earth", "second": "sugar"}).content)
# print(chain.invoke({"first": "Water", "second": "Fire"}).content)


class Ingredient:
    def __init__(self, name: str, ingredients: list[str]):
        self.name = name
        self.ingredients = set(ingredients)
        self.used_in = set()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f"Ingredient({self.name}, Made from: {self.ingredients})"
    
    def __repr__(self):
        return str(self)
    


# visited = set(["Water", "Fire", "Wind", "Earth"])
recipes = set()
ingredients = set([
    Ingredient("Water", []),
    Ingredient("Fire", []),
    Ingredient("Wind", []),
    Ingredient("Earth", []),
])
visited = set()

stop = False
while not stop:
    print("Starting new loop")
    user_input = input("enter anything to quit")
    if user_input:
        stop = True
    
    for first in ingredients.copy().difference(visited):
        visited.add(first)
        for second in ingredients.copy():
            key = first.name + second.name
            if key in recipes:
                continue

            user_input = input("enter anything to quit")
            if user_input:
                stop = True

            combo = chain.invoke({"first": first.name, "second": second.name}).content
            new_ingredient = Ingredient(combo, [first.name, second.name])
            ingredients.add(new_ingredient)
            first.used_in.add(new_ingredient)
            second.used_in.add(new_ingredient)
            recipes.add(key)
            recipes.add(second.name + first.name)
            print(f"Crafted {new_ingredient.name} from {first.name} and {second.name}")

