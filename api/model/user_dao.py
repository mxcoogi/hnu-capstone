from sqlalchemy import text

class UserDao:
    def __init__(self, database):
        self.db = database
    
    def insert_user(self, user):
        with self.db.connect() as connection:
            connection.execute(text("""
                INSERT INTO users(
                    student_id,
                    name,
                    hashed_password
                ) VALUES(
                    :student_id,
                    :name,
                    :password
                )
            """), user).lastrowid

            connection.commit()
        
        with self.db.connect() as connection:
            connection.execute(text("""
                INSERT INTO user(
                    student_id,
                    name,
                    hashed_password
                ) VALUES(
                    :student_id,
                    :name,
                    :password
                )
            """), user).lastrowid

            connection.commit()
        

    def get_user_id_and_password(self, student_id):
        with self.db.connect() as connection:
            row = connection.execute(text(
                'SELECT student_id, hashed_password FROM users WHERE student_id = :student_id'
            ), {'student_id' : student_id}).fetchone()

        return {
            'student_id' : row[0],
            'hashed_password' : row[1]
        } if row else None


    def get_user_info(self, student_id):
        with self.db.connect() as connection:
            row = connection.execute(text(
                'SELECT student_id, name, average_grade, department, volunteer_hours FROM user WHERE student_id = :student_id'
            ), {'student_id' : student_id}).fetchone()

        return {
            'student_id' : row[0],
            'name' : row[1],
            'average_grade' : row[2],
            'department' : row[3],
            'volunteer_hours' : row[4]
        } if row else None