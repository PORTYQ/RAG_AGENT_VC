from  sqlalchemy import Integer,String
from pathlib import Path
import pandas as pd
from connection import engine
def load_csv_to_sqlite(csv_path:str,table_name:str):
    df = pd.read_csv(csv_path)
    if 'id' not in df.columns:
        df.insert(0,'id',range(1,len(df)+1))

    df.to_sql( 
        table_name,
        con=engine,
        if_exists = 'replace',
        index = False,
        dtype ={
        'id':Integer(),
        'Год':Integer(),
        "Спутник":String(),
        "Площадь с растительностью, кв. м":String(),
        "Площадь без растительности, кв. м":String(),
        "%A":String(),
        "1 - %A":String(),
        "%B":String(),
        "1 - %B":String(),
        }
     )    
def main():
    for p in Path('data').glob('*.csv'):
        load_csv_to_sqlite(str(p),p.stem)


if __name__ == '__main__':
    pass