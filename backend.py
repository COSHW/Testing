import psycopg2


class Database_user:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='testing' user='postgres' password='Lovunod2302' host='localhost' port='5432'")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email varchar(50) UNIQUE , password varchar(50), points_mat int, points_rus int, points_eng int, points_inf int, root text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS mat (id SERIAL PRIMARY KEY, question text , answer1 text, answer2 text, answer3 text, answer4 text, dif_points text, level text, explanation text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS rus (id SERIAL PRIMARY KEY, question text , answer1 text, answer2 text, answer3 text, answer4 text, dif_points text, level text, explanation text)")
        # self.cur.execute("CREATE TABLE IF NOT EXISTS eng (id SERIAL PRIMARY KEY, question text , answer1 text, answer2 text, answer3 text, answer4 text, dif_points text, level text, explanation text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS inf (id SERIAL PRIMARY KEY, question text , answer1 text, answer2 text, answer3 text, answer4 text, dif_points text, level text, explanation text)")
        self.cur.execute("create table if not exists Locations (lat text, lon text, message text)")
        self.conn.commit()

        self.cur.execute("SELECT COUNT(*) AS rows FROM mat")
        rows1 = self.cur.fetchall()
        if rows1[0][0] == 0:
            mat_file = open("off_data/Math.txt", "rb")
            for line in mat_file:
                x = line.decode().split(";")
                self.cur.execute("insert into mat (question, answer1, answer2, answer3, answer4, dif_points, level, explanation) values (%s,%s,%s,%s,%s,%s,%s,%s)", (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
                self.conn.commit()
        self.cur.execute("SELECT COUNT(*) AS rows FROM rus")
        rows2 = self.cur.fetchall()
        if rows2[0][0] == 0:
            rus_file = open("off_data/Russian.txt", "rb")
            for line in rus_file:
                x = line.decode().split(";")
                self.cur.execute("insert into rus (question, answer1, answer2, answer3, answer4, dif_points, level, explanation) values (%s,%s,%s,%s,%s,%s,%s,%s)", (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
                self.conn.commit()
        # self.cur.execute("SELECT COUNT(*) AS rows FROM eng")
        # rows3 = self.cur.fetchall()
        # if rows3[0][0] == 0:
        #     pass
        self.cur.execute("SELECT COUNT(*) AS rows FROM inf")
        rows4 = self.cur.fetchall()
        if rows4[0][0] == 0:
            rus_file = open("off_data/IT.txt", "rb")
            for line in rus_file:
                x = line.decode().split(";")
                self.cur.execute("insert into inf (question, answer1, answer2, answer3, answer4, dif_points, level, explanation) values (%s,%s,%s,%s,%s,%s,%s,%s)", (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
                self.conn.commit()
        self.cur.execute("SELECT COUNT(*) AS rows FROM Locations")
        rows5 = self.cur.fetchall()
        if rows5[0][0] == 0:
            locations_file = open("off_data/Locations.txt", "rb")
            for line in locations_file:
                x = line.decode().split(";")
                self.cur.execute("insert into Locations values (%s,%s,%s)", (x[0], x[1], x[2]))
                self.conn.commit()

    def check_email(self, email):
        self.cur.execute("select * from users where email like %s", (email, ))
        result = self.cur.fetchall()
        return result

    def register(self, email, password):
        self.cur.execute("INSERT INTO users (email, password, points_mat, points_rus, points_eng, points_inf, root) VALUES (%s, %s, 0, 0, 0, 0, 'user')", (email, password))
        self.conn.commit()

    def check(self, email, password):
        self.cur.execute("SELECT * FROM users WHERE email like %s and password like %s", (email, password))
        result = self.cur.fetchall()
        return result

    def check_user_points(self, subject, email):
        if subject == "mat":
            subject = "points_mat"
        elif subject == "rus":
            subject = "points_rus"
        elif subject == "eng":
            subject = "points_eng"
        elif subject == "inf":
            subject = "points_inf"
        self.cur.execute("select %s from users where email like %s", (subject, email))
        result = self.cur.fetchall()
        return result

    def check_all_user_points(self, email):
        self.cur.execute("select points_mat, points_rus, points_eng, points_inf from users where email like %s", (email, ))
        result = self.cur.fetchall()
        return result

    def view(self, subject):
        rows = "error"
        if subject == "":
            pass
        else:
            self.cur.execute("select * from " + subject)
            rows = self.cur.fetchall()
        return rows

    def insert(self, subject, question, answer1, answer2, answer3, answer4, dif_points, level):
        self.cur.execute("insert into " + subject + " (question, answer1, answer2, answer3, answer4, dif_points, level) values(%s, %s, %s, %s, %s, %s, %s)", (question, str(answer1), str(answer2), str(answer3), str(answer4), dif_points, level))
        self.conn.commit()

    def update(self, subject, q_id, question, answer1, answer2, answer3, answer4, dif_points, level):
        self.cur.execute("update " + subject + " set question = %s, answer1 = %s, answer2 = %s, answer3 = %s, answer4 = %s, dif_points = %s, level = %s where id = %s", (question, str(answer1), str(answer2), str(answer3), str(answer4), dif_points, level, q_id))
        self.conn.commit()

    def delete(self, subject, q_id):
        self.cur.execute("delete from " + subject + " where id = %s", (q_id, ))
        self.conn.commit()

    def question_pool(self, subject, level):
        self.cur.execute("select * from " + subject + " where level = %s and dif_points = '10' ORDER BY random() limit 2", (str(level), ))
        result1 = self.cur.fetchall()
        self.cur.execute("select * from " + subject + " where level = %s and dif_points = '15' ORDER BY random() limit 2", (str(level),))
        result2 = self.cur.fetchall()
        self.cur.execute("select * from " + subject + " where level = %s and dif_points = '25' ORDER BY random() limit 2", (str(level),))
        result3 = self.cur.fetchall()
        result = result1 + result2 + result3
        return result

    def add_points(self, subject, email, level):
        if subject == "mat":
            subject = "points_mat"
        elif subject == "rus":
            subject = "points_rus"
        elif subject == "eng":
            subject = "points_eng"
        elif subject == "inf":
            subject = "points_inf"
        self.cur.execute("select " + subject + " from users where email like %s", (email, ))
        result = self.cur.fetchall()
        result = int(result[0][0]/10) + 1
        if result == level or level == 0:
            self.cur.execute("update users set " + subject + " = " + subject + " + 10 where email like %s", (email, ))
            self.conn.commit()

    def map_markers(self):
        self.cur.execute("select * from Locations")
        result = self.cur.fetchall()
        return result

    def ege_pool_mat(self, subject="mat"):
        result = list()
        self.cur.execute("select * from " + subject + " where level = '1' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '1' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '2' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '2' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '3' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '3' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '4' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '4' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        return result

    def ege_pool(self, subject):
        result = list()
        self.cur.execute("select * from " + subject + " where level = '1' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '1' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '1' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '2' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '2' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '2' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '3' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '3' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '3' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '4' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '4' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '4' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '5' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '10' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '15' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        self.cur.execute("select * from " + subject + " where level = '6' and dif_points = '25' ORDER BY random() limit 1")
        result.append(self.cur.fetchall()[0])
        return result

    def add_final_points(self, subject, email, points):
        if subject == "mat":
            subject = "points_mat"
        elif subject == "rus":
            subject = "points_rus"
        elif subject == "eng":
            subject = "points_eng"
        elif subject == "inf":
            subject = "points_inf"
        self.cur.execute("update users set " + subject + " = " + points + " where email like %s", (email, ))
        self.conn.commit()
