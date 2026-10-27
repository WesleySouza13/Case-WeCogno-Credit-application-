import pandas as pd 
import os 
import sqlite3 
raw_path = os.path.join('data', 'processed')
data_dir = os.scandir(raw_path)
db_path = os.path.join('src', 'analytics', 'CreditDatabase.db')
con = sqlite3.connect(db_path)

for dir in data_dir:
    if dir.is_file() and dir.name.endswith('.parquet'):
        print(f'aquivo {dir.name} encontrado')
        table_name = os.path.splitext(dir.name)[0]
        df = pd.read_parquet(dir)
        df.to_sql(table_name, con, if_exists='replace', index=False)
        print(f'tabela {table_name} criada com sucesso')
    else:
        print('nenhum arquivo encontrado')
con.close()