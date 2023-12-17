import requests
import os
import json
from dotenv import load_dotenv
from work_items import work_item_ids
# work_orders_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_orders/{work_order_id}'
# work_packages_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_packages/{work_package_id}'

def fetch_work_items_from_api():
    print("Fetching work items data from api...")
    work_items_url= 'https://staging.api.vitruvi.cc/api/v1/wbs/work_items/{work_item_id}'
    load_dotenv()
    bearer_token = os.getenv("BEARER_TOKEN")
    headers = {
        "Authorization":f"Bearer {bearer_token}",
        "Content-Type":"application/json"
    }
    work_items_data = {}
    for work_item_id in work_item_ids:
        # api_url = work_items_url.format(work_item_id = work_item_id)
        response = requests.get(work_items_url.format(work_item_id = work_item_id), headers=headers)

        if response.status_code == 200:
            data = response.json()
            work_items_data[work_item_id] = data
        else:
            print(f"Failed to retrieve data for {work_item_id}: ", response.status_code)
    return work_items_data

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_data_from_file(filename):
    with open(filename,'r') as file:
        return json.load(file)

def count_completed_work_items(work_items_data):
    work_packages = set()
    for work_item in work_items_data.values():
        work_packages.add(work_item['work_package'])

    completed_items = {wp: 0 for wp in work_packages}

    for work_item in work_items_data.values():
        if work_item['status'] == 'completed':
            work_package_id = work_item['work_package']
            completed_items[work_package_id] += 1

    print("1) Completed work items per package:")
    for wp in work_packages:
        print(f"Work Package {wp}: {completed_items[wp]} completed items")


#-------------------------------------------------------------------------------
data_filename = 'work_items_data.json'
if os.path.exists(data_filename):
    work_items_data = load_data_from_file(data_filename)
else:
    work_items_data = fetch_work_items_from_api()
    save_data_to_file(work_items_data,data_filename)


count_completed_work_items(work_items_data)