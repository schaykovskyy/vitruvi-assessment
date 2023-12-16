import requests
import os
import json
from dotenv import load_dotenv
from work_items import work_item_ids

work_items_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_items/{work_item_id}'
work_orders_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_orders/{work_order_id}'
work_packages_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_packages/{work_package_id}'

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")
headers = {
    "Authorization":f"Bearer {bearer_token}",
    "Content-Type":"application/json"
}

work_items_data={}
for work_item_id in work_item_ids:
    # api_url = work_items_url.format(work_item_id = work_item_id)
    response = requests.get(work_items_url.format(work_item_id = work_item_id), headers=headers)

    if response.status_code == 200:
        data = response.json()
        work_items_data[work_item_id] = data
    else:
        print(f"Failed to retrieve data for {work_item_id}: ", response.status_code)

with open('work_items_data.json', 'w') as file:
    json.dump(work_items_data, file)

# with open('work_items_data.json','r') as file:
#     work_items_data = json.load(file)
