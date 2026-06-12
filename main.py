from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd

app = FastAPI(title="Chess Prediction API")

class ChessData(BaseModel):
    rating_diff: float

@app.post("/predict")
def predict_winner(data: ChessData):
    input_data = pd.DataFrame([{"rating_diff": data.rating_diff}])
    
    try:
        # აქ მოგვიანებით ჩასვამ შენს RUN_ID-ს
        run_id = "222e75f12433463682171567e9bf3c8b" 
        model_uri = f"runs:/{run_id}/model"
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        
        prediction = loaded_model.predict(input_data)
        return {"prediction": int(prediction[0]), "status": "success"}
    except Exception as e:
        return {"error": str(e), "message": "შეამოწმე RUN_ID."}