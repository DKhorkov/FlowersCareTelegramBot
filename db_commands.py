import sqlite3


class DataBase:

    def __init__(self):
        self.connection = sqlite3.connect("mydatabase.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL, user_name TEXT,
         user_surname TEXT, username TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS flowers (user_id INTEGER NOT NULL, flower_name TEXT NOT NULL,
         flower_type TEXT, flower_watering_interval INTEGER NOT NULL, flower_watering_last_time DATETIME)''')
        self.connection.commit()

    def check_if_user_is_already_in_database(self, user_id):
        self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        data = self.cursor.fetchone()
        return data

    def add_user_to_database(self, message):
        user_info = [message.chat.id, message.from_user.first_name, message.from_user.last_name,
                     message.from_user.username]
        self.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user_info)
        self.connection.commit()

    def add_flower_info_to_database(self, user_id, flower_name, flower_type, flower_watering_interval, current_time):
        flower_info_list = [user_id, flower_name, flower_type, flower_watering_interval, current_time]
        self.cursor.execute("INSERT INTO flowers VALUES(?, ?, ?, ?, ?);", flower_info_list)
        self.connection.commit()

    def selecting_flowers_from_database(self, user_id):
        user_id = [user_id]
        result = self.cursor.execute("SELECT * FROM flowers WHERE user_id = ?", user_id)
        return result.fetchall()

    def update_flower_last_time_watering(self, user_id, flower_name, flower_type, last_watered_time):
        info_list = [last_watered_time, user_id, flower_name, flower_type]
        sql = """
        UPDATE flowers 
        SET flower_watering_last_time = ?
        WHERE user_id = ? AND flower_name = ? AND flower_type = ?
        """
        self.cursor.execute(sql, info_list)
        self.connection.commit()

    def delete_flower_from_database(self, user_id, flower_name, flower_type):
        info_list = [user_id, flower_name, flower_type]
        sql = """
            DELETE FROM flowers 
            WHERE user_id = ? AND flower_name = ? AND flower_type = ?
            """
        self.cursor.execute(sql, info_list)
        self.connection.commit()

    def select_flower_from_database(self, user_id, flower_name, flower_type):
        info_list = [user_id, flower_name, flower_type]
        result = self.cursor.execute("SELECT * FROM flowers WHERE user_id = ? AND flower_name = ? AND flower_type = ?",
                                     info_list)
        return result.fetchone()

    def select_all_flowers(self):
        sql = '''SELECT * FROM flowers'''
        result = self.cursor.execute(sql)
        return result.fetchall()
