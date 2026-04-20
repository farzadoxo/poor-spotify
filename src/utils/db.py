# import sqlite3 


# con = sqlite3.connect('db.sqlite3')
# cur = con.cursor()


# class File:
#     def __init__(self,name,url,format):
#         self.name = name
#         self.url = url
#         self.format = format



# def insert_music(file:File):
#     cur.execute(f"INSERT INTO music_music(name,url,format) VALUES ('{file.name}','{file.url}','{file.format}')")
#     con.commit()


# # if __name__ == "__main__":
# #     cur.execute("CREATE TABLE IF NOT EXISTS music_music (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL , url TEXT NOT NULL , format TEXT NOT NULL)")
# #     con.commit()