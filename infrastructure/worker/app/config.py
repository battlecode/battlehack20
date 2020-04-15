import os
import logging

# Configure logging format

logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
logging.getLogger().setLevel(logging.INFO)


# Constants, parameters and configurations

GCLOUD_PROJECT_ID        = 'battlecode18'
GCLOUD_SUB_COMPILE_NAME  = 'bc20-compile-sub'
GCLOUD_SUB_GAME_NAME     = 'bc20-game-sub'
GCLOUD_BUCKET_SUBMISSION = 'bc20-submissions'
GCLOUD_BUCKET_REPLAY     = 'bc20-replays'

SUB_ACK_DEADLINE = 30 # Value to which ack deadline is reset
SUB_SLEEP_TIME   = 10 # Interval between checks for new jobs and ack deadline

TIMEOUT_UNZIP   = 30    # Maximum execution time for unzipping submission archive
TIMEOUT_PULL    = 150   # Maximum execution time for updating distribution
TIMEOUT_COMPILE = 300   # Maximum execution time for submission compilation
TIMEOUT_GAME    = 10800 # Maximum execution time for game running

GAME_WINNER = '^\[server\]\s*.*\([AB]\) wins \(round [0-9]+\)$'

API_AUTHENTICATE = 'https://bh2020.battlecode.org/auth/token/'
API_USERNAME = os.getenv('BC20_DB_USERNAME')
API_PASSWORD = os.getenv('BC20_DB_PASSWORD')


# Compilation API specifications

COMPILE_SUCCESS = 1
COMPILE_FAILED  = 2
COMPILE_ERROR   = 3
def api_compile_update(submissionid):
    """
    Returns the API link for reporting the compilation status
    submissionid: the ID of the submission
    """
    return 'https://bh2020.battlecode.org/api/0/submission/{}/compilation_update/'.format(submissionid)

# Game running API specifications

GAME_REDWON  = 'redwon'
GAME_BLUEWON = 'bluewon'
GAME_ERROR   = 'error'
def api_game_update(gametype, gameid):
    """
    Returns the API link for reporting the compilation status
    gametype: 'scrimmage' or 'tournament'
    gameid: the ID of the game
    """
    return 'https://bh2020.battlecode.org/api/0/{}/{}/set_outcome/'.format(gametype, gameid)
