import sqlite3

class Database:
    def __init__(self, db="media.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, title TEXT, creator TEXT, date TEXT, media_path TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, title TEXT, creator TEXT, date TEXT, media_path TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, title TEXT, creator TEXT, date TEXT, media_path TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS audio (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, title TEXT, creator TEXT, date TEXT, media_path TEXT)")
        self.conn.commit()
        self.conn.close()

    def fetch(self, searchlist):
        self.conn = sqlite3.connect("media.db")
        self.cur = self.conn.cursor()
        media_type = searchlist[0]
        media_type = media_type.lower()
        if len(searchlist) == 1:
            query = f"SELECT * FROM {media_type};"
        query = f"SELECT * FROM {media_type}"
        if searchlist:
            queries = searchlist[1:]
            for  item in range(len(queries)):
                if queries[item] == queries[0] and queries[item] != queries[-1]:
                    query += f" WHERE {queries[item]} AND"
                elif queries[item] == queries[0] and queries[item] == queries[-1]:
                    query += f" WHERE {queries[item]};"
                elif queries[item] == queries[-1]:
                    query += f" {queries[item]};"
                else:
                    query += f" {queries[item]} AND"        
        # print(query)

        self.cur.execute(query)
        results = self.cur.fetchall()
        self.conn.close()
        # print(results)
        return results
    
    def insert(self, media_type, country, title, creator, date, media_path):
        self.conn = sqlite3.connect("media.db")
        self.cur = self.conn.cursor()
        self.cur.execute(f"INSERT INTO {media_type} (country, title, creator, date, media_path) VALUES (?, ?, ?, ?, ?)", (country, title, creator, date, media_path))
        self.conn.commit()
        self.conn.close()

