import logging, json, unittest, os, sys
import pandas as pd
from typing import Any, Dict

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Add this path first so it picks up the newest changes without having to rebuild
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, this_dir + "/..")
from umich_api.api_utils import ApiUtil

CONFIG_PATH: str = os.path.join(this_dir, os.getenv('ENV_FILE', 'env.json'))

# Set up ENV and ENV_SCHEMA
try:
    with open(CONFIG_PATH) as env_file:
        ENV: Dict[str, Any] = json.loads(env_file.read())
except FileNotFoundError:
    logger.error(f'Configuration file could not be found; please add file "{CONFIG_PATH}".')
    ENV = dict()

# use API inside UM API directory
API_BASE_URL = ENV["API_BASE_URL"]
API_CLIENT_ID = ENV["API_CLIENT_ID"]
API_CLIENT_SECRET = ENV["API_CLIENT_SECRET"]
API_SCOPE_PREFIX = ENV["API_SCOPE_PREFIX"]
API_SUBSCRIPTION_NAME = ENV["API_SUBSCRIPTION_NAME"]
API_UTIL = ApiUtil(API_BASE_URL, API_CLIENT_ID, API_CLIENT_SECRET)

# max attempts
MAX_REQ_ATTEMPTS = ENV["MAX_REQ_ATTEMPTS"]

# the csv consists of four columns: 'Uniqname', 'Last Name', 'First Name', 'Title'
df = pd.read_csv("user.csv")

global_pd= pd.DataFrame(columns=('Uniqname', 'Last Name', 'First Name', 'Title', 'User ID'))

# iterate through the user csv file, do user SIS Id lookup
for index, row in df.iterrows():
    sis_user_id=None

    lastName = row['Last Name']
    firstName = row['First Name']
    title = row['Title']
    uniqname=row['Uniqname']

    # url for API call
    url = f'{API_SCOPE_PREFIX}/accounts/1/users?search_term={uniqname}'

    logger.info(url)
    for i in range(1, MAX_REQ_ATTEMPTS + 1):
        logger.info(f'Attempt #{i}')
        response = API_UTIL.api_call(url, API_SUBSCRIPTION_NAME, payload={})
        status_code = response.status_code
        
        if status_code != 200:
            logger.info(url)
            logger.warning(f'Received irregular status code: {url} {status_code}')
            logger.info('Beginning next_attempt')
        else:
            try:
                users = json.loads(response.text)
                for user in users:
                    logger.info(uniqname + " " + user['login_id'])
                    if user['login_id'] == uniqname:
                        sis_user_id = user['sis_user_id']
                        break
            except JSONDecodeError:
                logger.warning('JSONDecodeError encountered')
                logger.info('Beginning next attempt')
            
            # API call was a success, no need to call again
            break


    # added to output dataframe
    user_dict = {
                'Uniqname': uniqname,
                'Last Name': lastName,
                'First Name': firstName,
                'Title': title,
                'User ID': sis_user_id}
    global_pd = global_pd.append(user_dict, ignore_index=True)
    global_pd.to_csv("./user_with_id.csv")