from os import environ
import logging
import socketio
import uuid

logger = logging.getLogger("Settings")

def init():
    logger.info("Settings file initiated")
    # Main programs
    global firmataProgram
    global socketProgram

    # Static variables
    global GUID
    global SERVER_URL
    global SERVER_ROBOT_SECRET
    global ACCESS_TOKEN
    global INPUT_PIN
    global OUTPUT_PIN

    # Dynamic variables
    global sio
    global programStarted
    global programRunning
    global disconnectCount

    # Initialize static variables
    GUID = str(uuid.uuid4())
    SERVER_URL = environ.get("SERVER_URL")
    SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
    INPUT_PIN = environ.get("INPUT_PIN")
    OUTPUT_PIN = environ.get("OUTPUT_PIN")

    # Initialize dynamic variables
    firmataProgram = None
    socketProgram = None

    sio = socketio.Client(reconnection_attempts=10)
    programStarted = True
    programRunning = False
    disconnectCount = 0

    # Variable checking
    # Must-provide variables
    if SERVER_URL is None:
        logger.critical("SERVER_URL not provided as environment variable")
        raise ValueError("SERVER_URL should be provided as environment variable")
    elif SERVER_ROBOT_SECRET is None:
        logger.critical("SERVER_ROBOT_SECRET not provided as environment variable")
        raise ValueError("SERVER_ROBOT_SECRET should be provided as environment variable")

    # Optional variables
    if INPUT_PIN is None:
        logger.info("INPUT_PIN not provided, defaults to d:0:o")
        INPUT_PIN = "d:0:o"
    else:
        logger.info(f"INPUT_PIN is {INPUT_PIN}")
    if OUTPUT_PIN is None:
        logger.info("OUTPUT_PIN not provided, defaults to d:0:i")
        OUTPUT_PIN = "d:0:i"
    else:
        logger.info(f"OUTPUT_PIN is {OUTPUT_PIN}")

if __name__ == "__main__":
    logger.critical("Module hnr_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")