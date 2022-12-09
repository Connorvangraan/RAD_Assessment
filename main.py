from radio_module import Radio
from user_module import User
from flask import *


# Initialise the Flask module
app = Flask(__name__)


@app.route('/radio_stations/', methods=['GET'])
def get_radio_station_address() -> dict:
    """
    API endpoint to retrieve radio link.
    Station name is supplied in the request as: /radio_stations/?station=STATION_NAME
    :return: dictionary containing the id, name and link for the given radio station
    """

    user_query = str(request.args.get('station'))
    print(user_query)

    return radio.get_station(user_query)

# List endpoint
@app.get('/radio_stations')
def list_radio_stations() -> dict:
    """
    Retrieves all of the radio stations; ids, names and links
    :return: dictionary of stations
    """
    return radio.list_stations()

# Get one endpoint
@app.route('/user/', methods=['GET'])
def get_user():
    """
    Retrieves the user data with login data supplied in the request in the format
    "/user/?user=USERNAME PASSWORD
    :return: dictionary containing user data
    """
    user_query = str(request.args.get('user'))
    return user.get_user(user_query)



if __name__ == '__main__':
    # intialise connection to the databases
    radio = Radio()
    user = User()

    # Open the API locally
    app.run(port=7777)
