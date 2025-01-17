#/
# 
#       This script is used to extract data from Mailchimp. API documentation:
#       https://mailchimp.com/developer/marketing/api/root/ 
#
# /#

# import libraries
import os
import json
import mailchimp_marketing
from datetime import datetime, timedelta
from dotenv import load_dotenv 
from mailchimp_marketing.api_client import ApiClientError

# load .env
load_dotenv()

# set api key
api_key = os.getenv('MAILCHIMP_API_KEY')

# ################################# Campaign Lists #####################################################

# build filename
now = datetime.now().strftime('%Y%m%d_%H%m%S')
file_name = './data/campaigns/' + f'data_campaign_list_{now}.json'

end_time = datetime.now().strftime('%Y-%m-%dT00:00:00')
start_time=datetime.now() - timedelta(days=1)
start_time=start_time.strftime('%Y-%m-%dT00:00:00')

print(start_time, end_time)

# extract json
try:
  client = mailchimp_marketing.Client()
  client.set_config({
    "api_key": api_key,
    "since_send_time" : start_time,
    "before_sent_time" : end_time
  })

  response = client.campaigns.list()
  with open(file_name, 'w') as file:
    json.dump(response, file, indent=4)
except ApiClientError as error:
  print("Error: {}".format(error.text))


campaign_ids = []
i = 0

while i < len(response['campaigns']):
  campaign_ids.append(response['campaigns'][i]['id'])
  i += 1

########################################################################################### emails

for cid in campaign_ids:
  # build filename
    now = datetime.now()
    now = now.strftime('%Y%M%d_%H%m%S')
    file_name = './data/emails/'+f'data_campaign_email_activity_{cid}_{now}.json'

    # extract json
    try:
        response = client.campaigns.get_content(cid)
        with open(file_name, 'w') as file:
            json.dump(response, file, indent=4)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

#################################################################################################unsubscribes

for cid in campaign_ids:
  # build filename
    now = datetime.now()
    now = now.strftime('%Y%M%d_%H%m%S')
    file_name = './data/unsubscribes/'+f'data_campaign_unsubscribes_{cid}_{now}.json'

    # extract json
    try:
        response = client.reports.get_unsubscribed_list_for_campaign(cid)
        with open(file_name, 'w') as file:
            json.dump(response, file, indent=4)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
  

############################################ Lists ##############################################################################

# build filename
now = datetime.now()
now = now.strftime('%Y%M%d_%H%m%S')
file_name = './data/lists/'+f'data_lists_{now}.json'

try:
  response = client.lists.get_all_lists()
  with open(file_name, 'w') as file:
    json.dump(response, file, indent=4)
except ApiClientError as error:
  print("Error: {}".format(error.text))

list_ids = []
i = 0

while i < len(response['lists']):
  list_ids.append(response['lists'][i]['id'])
  i += 1

################################################################################ list members

for lid in list_ids:
  # build filename
    now = datetime.now()
    now = now.strftime('%Y%M%d_%H%m%S')
    file_name = './data/listmembers/'+f'data_list_members_{lid}_{now}.json'

    # extract json
    try:
        response = client.lists.get_list_members_info(lid)
        with open(file_name, 'w') as file:
            json.dump(response, file, indent=4)
    except ApiClientError as error:
        print("Error: {}".format(error.text))

######################################################################################### Reports ####

# build filename
now = datetime.now()
now = now.strftime('%Y%M%d_%H%m%S')
file_name = './data/reports/'+f'data_reports_{now}.json'

try:
  response = client.reports.get_all_campaign_reports()
  with open(file_name, 'w') as file:
    json.dump(response, file, indent=4)
except ApiClientError as error:
  print("Error: {}".format(error.text))