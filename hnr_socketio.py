from os import environ
from main import GUID, sio
import logging

def start(guid, server_url, access_token):
    # Workaround for global variables as python-socketio functions are static functions
    environ['socketio-GUID'] = guid
    environ['socketio-SERVER_URL'] = server_url
    environ['socketio-ACCESS_TOKEN'] = access_token
    logging.info(f"Initiated Socket.IO connection with server, GUID is {guid}, server URL is {server_url},access token is {access_token}")

    sio.connect(server_url)
    sio.wait()

    print("An error occured while connection to the Socket.IO server. Please check the logs for more information.")
    logging.warning(f"Unable to connect to server through Socket.IO, deleting client data from database then exiting")
    # Delete data from database
    req_json = {
        "guid": guid,
        "token": access_token
    }
    req_response = requests.delete(f"{server_url}/access", json=req_json)
    req_code = req_response.status_code
    if req_code == 204:
        logging.info("Deletion request successful, client data deleted from database")
    elif req_code == 400:
        logging.error("Deletion request failed with error code 400 (Incorrect parameters)")
    elif req_code == 404:
        logging.error("Deletion request failed with error code 404 (Client could not be found)")
    elif req_code == 500:
        logging.error("Deletion request failed with error code 500 (Error occured while attempting to query database)")
    else:
        logging.error(f"Deletion request failed with unknown error code {req_code}")

@sio.event
def connect():
    logging.info("Socket.IO connection with server established, authenticating")
    sio.emit("authentication", { 
        "guid": environ['socketio-GUID'],
        "token": environ['socketio-ACCESS_TOKEN']
    })

@sio.event
def authenticated(data):
    logging.info("Authentication successful, starting the Arduino and PiCamera modules")

@sio.event
def unauthorized(data):
    logging.error(f"Unauthorized connect to server through Socket.IO, message is {data['message']}")

# TODO: Functions

@sio.event
def disconnect():
    logging.info("Disconnected from server")

if __name__ == "__main__":
    loggingS.critical("Module hnr_socketio ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")