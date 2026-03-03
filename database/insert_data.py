import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv

# Connection string
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS employees_full CASCADE"))
    conn.commit()

# Load CSVs
df_sirh = pd.read_csv(r'C:\Users\Kevin\projects\OC P4\Projet 4\extrait_sirh.csv')
df_eval = pd.read_csv(r'C:\Users\Kevin\projects\OC P4\Projet 4\extrait_eval.csv')
df_eval['eval_number'] = pd.to_numeric(df_eval['eval_number'].str[2:], errors='raise')
df_sondage = pd.read_csv(r'C:\Users\Kevin\projects\OC P4\Projet 4\extrait_sondage.csv')


# Insert into DB
df_sirh.to_sql('employees_sirh', engine, if_exists='replace', index=False)
df_eval.to_sql('employees_eval', engine, if_exists='replace', index=False)
df_sondage.to_sql('employees_sondage', engine, if_exists='replace', index=False)

print("Data inserted successfully!")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE OR REPLACE VIEW employees_full AS
        SELECT * FROM employees_sirh s
        INNER JOIN employees_sondage so ON s.id_employee = CAST(so.code_sondage AS INTEGER)
        INNER JOIN employees_eval e ON s.id_employee = CAST(e.eval_number AS INTEGER)
    """))
    conn.commit()

    print("View created successfully!")