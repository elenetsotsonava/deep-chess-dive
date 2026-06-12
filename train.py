import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import kagglehub

# 1. მონაცემების ჩატვირთვა Kaggle-დან
path = kagglehub.dataset_download("datasnaek/chess")
df = pd.read_csv(f"{path}/games.csv")

# მონაცემების მომზადება
df['white_higher'] = df['white_rating'] > df['black_rating']
df['higher_won'] = ((df['white_higher']) & (df['winner'] == 'white')) | \
                   ((~df['white_higher']) & (df['winner'] == 'black'))
df['rating_diff'] = df['white_rating'] - df['black_rating']

X = df[['rating_diff']]
y = df['higher_won'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. MLflow ექსპერიმენტის დაწყება
mlflow.set_experiment("Chess_Prediction_Experiment")

with mlflow.start_run() as run:
    model_penalty = 'l2'
    model = LogisticRegression(penalty=model_penalty)
    
    # პარამეტრის და მეტრიკის შენახვა (დავალების მოთხოვნა)
    mlflow.log_param("penalty", model_penalty)
    
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)
    
    # მოდელის შენახვა
    mlflow.sklearn.log_model(model, "model")
    
    print(f"მოდელი დატრენინგდა! სიზუსტე (Accuracy): {accuracy}")
    print(f"შენი RUN_ID არის: {run.info.run_id}")