from fastapi import FastAPI,UploadFile
import uvicorn
import pandas as pd




app = FastAPI()


@app.post("/upload")
def upload(file: UploadFile):
    df = pd.read_csv(file.file)
    df["level_risk"] = df["range_km"].apply(
        lambda x:  "low" if x <= 20 else (
            "medium" if 20 < x <= 100 else (
                "high" if 100 < x <= 300 else "extreme")))
    print(df.head())
    return "hi😊😊"

if __name__=="__main__":
    uvicorn.run(app)