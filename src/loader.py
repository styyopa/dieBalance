import csv


def load_foods():

    foods = []

    with open("data/foods.csv", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            food = {
                "name": row["name"],
                "carbs": float(row["Carbohydrates"]),
                "sugar": float(row["Glycemic Index"]),
                "protein": float(row["Protein"])
            }

            foods.append(food)

    return foods