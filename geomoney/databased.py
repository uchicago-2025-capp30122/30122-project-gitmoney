import sqlite3
import csv
import os 
import pathlib
import pandas as pd


def sql_csv(csv_fp):
    rlst = []
    with open(csv_fp, 'r', encoding='utf8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            rlst.append(tuple(line))
    return rlst
            

if __name__ == "__main__":
    
    cwd = pathlib.Path(os.getcwd())
    alder_csv_fp = cwd / r"Scraper/alders_2012_2023.csv"
    csv_data = sql_csv(alder_csv_fp)
    con = sqlite3.connect("./data/gitmoney_database.db")
    cursor = con.cursor()
    #df = pd.read_csv(alder_csv_fp)
    #cursor.execute("DROP TABLE IF EXISTS aldermanic")
    #df.to_sql('aldermanic', con, if_exists='append', index=False)
    #cursor.execute("CREATE TABLE IF NOT EXISTS alder (id TEXT, Ward TEXT, Alderperson TEXT, StartDate TEXT, EndDate TEXT, Party TEXT, Notes TEXT, CleanWard TEXT, StartYear TEXT, EndYear TEXT)")
    #insert_query = """INSERT INTO alder ('id', 'Ward', 'Alderperson', 'StartDate', 'EndDate', 'Party', 'Notes', 'CleanWard', 'StartYear', 'EndYear') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    #cursor.executemany(insert_query,csv_data[1:])

    query = r"SELECT * FROM aldermanic"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        print(row)
    con.commit()
    con.close()

