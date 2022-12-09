import sqlalchemy as db
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Table, Column, Integer, MetaData, String


def create_user_database():
    """
    Creates a database sqlite file and adds 3 users
    """
    engine = create_engine('sqlite:///data/users.sqlite', echo=True)

    metadata = MetaData()
    my_table = Table('users', metadata,
                     Column("id", Integer, autoincrement=True, primary_key=True),
                     Column('fname', String),
                     Column("lname", String),
                     Column("phone_num", String),
                     Column("email", String),
                     Column("password", String)
                     )

    metadata.create_all(engine)

    # generates insert queries to add the users
    insert_query = my_table.insert()
    engine.execute(insert_query, {"fname":'Francis', "lname":'Ngannou', "phone_num":'024898114527',"email":'fn@gmail.com', "password":'heavyweight_champ'})

    insert_query = f"INSERT INTO users values(null,'Ronald', 'McDonald', '014892111327','ronny@maccies.com', 'lovin_it')"
    engine.execute(insert_query, {"fname":'Ronald', "lname":'McDonald', "phone_num":'014892111327',"email":'ronny@maccies.com', "'lovin_it":'heavyweight_champ'})

    insert_query = f"INSERT INTO users values(null,'Keyser', 'Söze', '033338114527','keyser.söze@gmail.com', 'verbal')"
    engine.execute(insert_query, {"fname":'Keyser', "lname":'Söze', "phone_num":'033338114527',"email":'keyser.söze@gmail.com', "verbal":'heavyweight_champ'})


class User:
    def __init__(self):
        """
        User handles interactions with the user database
        """
        self.engine = db.create_engine(
            'sqlite:///data/users.sqlite')  # ensure this is the correct path for the sqlite file.

    # GET ALL
    def list_users(self) -> dict:
        """
        Gets all users from the database
        :return: Dictionary of user database
        """
        return pd.read_sql('SELECT * FROM users', self.engine).to_dict('index')

    # GET
    def get_user(self, user: str) ->  dict:
        """
        Gets single user entry
        :param user: user name and password separated by a space
        :return: dictionary with user details
        """
        try:
            email, password = user.split(" ")[0], user.split(" ")[1]
            return \
            pd.read_sql(f'SELECT * FROM users WHERE email = "{email}" AND password="{password}"', self.engine).to_dict(
                "index")[0]
        except KeyError:
            return {"USER NOT FOUND":0}
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # SET
    def set_user(self, fname: str, lname: str, phone_num: str, email: str, password: str):
        """
        Adds new user to the database
        :param fname:
        :param lname:
        :param phone_num:
        :param email:
        :param password:
        """
        insert_query = f"INSERT INTO users values(null,'{fname}', '{lname}', {phone_num}, '{email}', '{password}')"
        try:
            self.engine.execute(insert_query)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # UPDATE
    def update_user(self, user: str, new_data: dict):
        """
        Update the user data in the database
        :param user: email and password separated by space
        :param new_data: dictionary with new data
        """
        data = self.get_user(user)
        try:
            data.update(new_data)
        except AttributeError:
            return "ENTRY NOT FOUND"

        email,password = user.split()[0],user.split()[1]
        update_query = f"UPDATE users SET fname='{data['fname']}', lname='{data['lname']}', phone_num='{data['phone_num']}', password='{data['password']}' WHERE email = '{email}' AND password = '{password}'"
        try:
            self.engine.execute(update_query)
            return data
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # DELETE
    def delete_user(self, user: str):
        """
        Remove user entry from the database
        :param user: email and password separated by space
        """
        email, password = user.split(" ")[0], user.split(" ")[1]
        delete_query = f"DELETE FROM users WHERE email = '{email}' AND password = '{password}'"
        try:
            self.engine.execute(delete_query)
            return 1
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)


