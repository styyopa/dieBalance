import csv

def save_float(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return 0.0 
    
def load_foods():

    foods = []

    with open("data/foods.csv", newline="", encoding="utf-8") as file:
        
        reader = csv.DictReader(file)
        
        for row in reader:
            
            food = {
                "name": row("name"),
                "carbs": save_float(row("Carbohydrates")),
                "glycemic_index": save_float(row("Glycemic Index")),
                "protein": save_float(row("Protein")),
                "fiber": save_float(row("Fiber")),
                "fat": save_float(row("Fat")) 
            }
    
        foods.append(food)

    return foods