import sqlalchemy as db
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import csv


def create_radio_database():
    """
    Creates an sqlite file and it with the contents of the stations csv file
    """
    engine = db.create_engine('sqlite:///data/stations.sqlite', echo=True)

    metadata = db.MetaData()
    my_table = db.Table('radio_stations', metadata,
                        db.Column("id", db.Integer, autoincrement=True, primary_key=True),
                        db.Column('name', db.String),
                        db.Column('link', db.String),
                        )
    metadata.create_all(engine)
    insert_query = my_table.insert()

    # the contents of station.csv is inserted into the sqlite file
    with open('data/stations.csv', 'r', encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        engine.execute(
            insert_query,
            [{"id": i, "name": row[0], "link": row[1]}
             for i, row in enumerate(csv_reader)]
        )


class Radio:
    def __init__(self):
        """
        Radio handles access to the radio station database
        """
        self.engine = db.create_engine('sqlite:///data/stations.sqlite')

    # GET ALL
    def list_stations(self):
        """
        :return: dictionary containing all of the radio stations
        """
        return pd.read_sql('SELECT * FROM radio_stations', self.engine).to_dict('index')

    # GET
    def get_station(self, station: str):
        """
        Gets the data on the specified station
        :param station: name of the station
        :return: dictionary containing the station data
        """
        try:
            return pd.read_sql(f'SELECT * FROM radio_stations WHERE name = "{station}"', self.engine).to_dict("index")[
                0]
        except KeyError:
            return "STATION NOT FOUND"
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # SET
    def set_station(self, station_name: str, station_link: str):
        """
        Add new station to the database
        :param station_name: name of the station
        :param station_link: hyperlink for the station
        """
        insert_query = f"INSERT INTO radio_stations values(null,'{station_name}', '{station_link}')"
        try:
            self.engine.execute(insert_query)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # UPDATE
    def update_station(self, station_name: str, new_link: str, new_name: str=""):
        """
        Changes the values stored in the database entry
        :param station_name: name of the station
        :param new_link: new link to store
        :param new_name: new name of the station
        :return:
        """
        old_link = self.get_station(station_name)
        if new_name != "":
            update_query = f"UPDATE radio_stations SET name = '{new_name}', link = '{new_link}' WHERE name = '{station_name}'"
        else:
            update_query = f"UPDATE radio_stations SET link = '{new_link}' WHERE name = '{station_name}'"
        try:
            self.engine.execute(update_query)
            return old_link
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    # DELETE
    def delete_station(self, station_name):
        """
        Deletes entry
        :param station_name:
        """
        delete_query = f"DELETE FROM radio_stations WHERE name = '{station_name}'"
        try:
            self.engine.execute(delete_query)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)


