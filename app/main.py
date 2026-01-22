from fastapi import FastAPI,UploadFile
import uvicorn
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="classicmodels"

)
mycursor = mydb.cursor()

a = """
    CREATE TABLE IF NOT EXISTS weapons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        weapon_id VARCHAR(50),
        weapon_name VARCHAR(50),
        weapon_type VARCHAR(50),
        range_km INT,
        weight_kg FLOAT,
        manufacturer VARCHAR(50),
        origin_country VARCHAR(50),
        storage_location VARCHAR(50),
        year_estimated INT,
        level_risk VARCHAR(50));
    """
mycursor.execute(a)





app = FastAPI()


@app.post("/upload")
def upload(file: UploadFile):
    a =0
    df = pd.read_csv(file.file)
    df["level_risk"] = df["range_km"].apply(
        lambda x:  "low" if x <= 20 else (
            "medium" if 20 < x <= 100 else (
                "high" if 100 < x <= 300 else "extreme")))
    df = df.fillna({"manufacturer":"Unknown"})
    my_data = df.to_dict("index")
    for itam in my_data:
        mycursor.execute("""
        INSERT INTO weapons (weapon_id,weapon_name,weapon_type,range_km,weight_kg,manufacturer,
		origin_country,storage_location,year_estimated,level_risk)
		VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s);""",
                         [itam[a]["weapon_id"],itam[a]["weapon_name"],itam[a]["weapon_type"],itam[a]["range_km"]
                             ,itam[a]["weight_kg"],itam[a]["manufacturer"],itam[a]["origin_country"]
                             ,itam[a]["storage_location"],itam[a]["year_estimated"],itam[a]["level_risk"]])
        a +=1


    return {f"status": "success","inserted_records": {a}}

if __name__=="__main__":
    uvicorn.run(app)