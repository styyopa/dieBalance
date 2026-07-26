# DiaBalance – AI Glycemic Risk Prediction System

DiaBalance is a machine learning project that predicts the glycemic risk of foods for people with Type 2 Diabetes based on their nutritional values.

The project uses a Random Forest Classifier trained on a public nutrition dataset to estimate whether a food represents a low, medium, or high glycemic risk. The prediction is then explained using rule-based nutritional analysis to provide understandable feedback for the user.

**Disclaimer:** This project is intended for educational purposes only and should not be used as medical advice.

---

## Features

- Machine Learning based food risk prediction
- Random Forest classifier
- Data preprocessing pipeline
- Prediction confidence using `predict_proba()`
- Human-readable explanation of predictions
- Personalized dietary recommendations
- Prediction history storage
- Modular and maintainable architecture

---

## Project Structure

```
DiaBalance/
│
├── data/
│   └── foods.csv
│
├── models/
│   └── model.pkl
│
├── src/
│   ├── loader.py
│   ├── preprocessing.py
│   ├── model_trainer.py
│   ├── predictor.py
│   ├── analyzer.py
│   ├── recommender.py
│   └── history.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## How It Works

```
Nutrition Dataset
        │
        ▼
Data Loader
        │
        ▼
Data Preprocessing
        │
        ▼
Random Forest Training
        │
        ▼
Saved Model
        │
        ▼
Food Prediction
        │
        ▼
Result Analysis
        │
        ▼
Diet Recommendation
```

---

## Machine Learning Pipeline

### Input Features

The model uses the following nutritional values:

- Carbohydrates
- Glycemic Index
- Protein
- Fiber
- Fat

### Model

- Algorithm: Random Forest Classifier
- Library: Scikit-learn
- Dataset: Public nutrition dataset

### Output

For each food the application predicts:

- Glycemic Risk
- Prediction Confidence
- Risk Score
- Nutritional Explanation
- Dietary Recommendation

Example:

```
Food: Apple

Prediction:
Low Glycemic Risk

Confidence:
95%

Risk Score:
5 / 100

Explanation:
- Low Glycemic Index
- Low Carbohydrate Content
- Healthy Fat Level

Recommendation:
Suitable as part of a balanced diet.
```

---

## Technologies

- Python 3
- Pandas
- NumPy
- Scikit-learn
- Joblib

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/DiaBalance.git
cd DiaBalance
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Train the Model

```bash
python src/model_trainer.py
```

The trained model will be saved to:

```
models/model.pkl
```

---

## Run the Application

```bash
python main.py
```

Example:

```
Enter food name:

Apple
```

Output:

```
Prediction Report

Prediction:
Low Glycemic Risk

Confidence:
95%

Risk Score:
5 / 100

Recommendation:
Suitable as part of a balanced diet.
```

---

## Future Improvements

- Support complete meals instead of individual foods
- Personalized recommendations based on user history
- Meal planning for an entire day
- Web interface using Flask or FastAPI
- Integration with real glycemic response datasets
- Explainable AI using SHAP values
- Mobile application

---

## Project Goals

The objective of DiaBalance is to demonstrate how machine learning can support healthier nutritional choices by analyzing food characteristics and estimating their glycemic risk.

This project was developed as an educational AI project and serves as a practical example of applying machine learning to nutrition-related data.

---

## License

This project is intended for educational purposes.