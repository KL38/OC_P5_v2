import pandas as pd
from sqlalchemy import create_engine 
#Column, Integer, String, Float, DateTime
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv
from create_db import Base

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
df_sondage = df_sondage.rename(columns={'code_sondage': 'id_employee'})
df_eval = df_eval.rename(columns={'eval_number': 'id_employee'})

with engine.connect() as conn:
    # Supprimer les FK si elles existent déjà
    conn.execute(text("ALTER TABLE employees_sondage DROP CONSTRAINT IF EXISTS fk_sondage_employee"))
    conn.execute(text("ALTER TABLE employees_eval DROP CONSTRAINT IF EXISTS fk_eval_employee"))
    conn.commit()

# Insert into DB
df_sirh.to_sql('employees_sirh', engine, if_exists='replace', index=False)
df_eval.to_sql('employees_eval', engine, if_exists='replace', index=False)
df_sondage.to_sql('employees_sondage', engine, if_exists='replace', index=False)

Base.metadata.create_all(engine, checkfirst=True)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE employees_sirh ADD PRIMARY KEY (id_employee)"))
    conn.execute(text("ALTER TABLE employees_sondage ADD CONSTRAINT fk_sondage_employee FOREIGN KEY (id_employee) REFERENCES employees_sirh(id_employee)"))
    conn.execute(text("ALTER TABLE employees_eval ADD CONSTRAINT fk_eval_employee FOREIGN KEY (id_employee) REFERENCES employees_sirh(id_employee)"))
    conn.commit()

print("Data inserted successfully!")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE OR REPLACE VIEW employees_full AS
        SELECT * FROM employees_sirh
        INNER JOIN employees_sondage USING(id_employee)
        INNER JOIN employees_eval USING(id_employee)
    """))
    conn.commit()

    print("View created successfully!")