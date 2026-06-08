import csv



def load_foods():

    foods = []

    with open("data/foods.csv", newline="", encoding="utf-8") as file:
        
        reader = csv.DictReader(file)

        for row in reader:
            def safe_float(value):
                try:
                    return float(value) if value else 0.0
                except ValueError:
                    return 0.0
            food = {
                "name": row["name"],
                "carbs": float(row["Carbohydrates"]),
                "glycemic_index": float(row["Glycemic Index"]),
                "protein": float(row["Protein"]),
                "fiber": float(row["Fiber"]),
                "fat": float(row["Fat"], 0)
            }

            foods.append(food)

    return foods