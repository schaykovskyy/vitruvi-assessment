import requests
import os
import json
from dotenv import load_dotenv
from work_items import work_item_ids
from datetime import datetime
import pandas as pd
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

#-------------------------------------------------------------------------------
data_filename = 'work_items_data.json'
if os.path.exists(data_filename):
    work_items_data = load_data_from_file(data_filename)
else:
    work_items_data = fetch_work_items_from_api()
    save_data_to_file(work_items_data,data_filename)

df = pd.read_json('work_items_data.json', orient='index')

print("\n1) Completed work items per package: ")
completed_items_count = df[df['status']== 'completed']['work_package'].value_counts()
print(completed_items_count)


print("\n2) Work order with most file data: ")
photos_df = df['photos'].apply(pd.Series)
photos_df = photos_df.stack().reset_index(level=1, drop=True).apply(pd.Series)

photos_df['file_size'] = photos_df['file_size'].fillna(0)
total_file_sizes = photos_df.groupby(df['work_order'])['file_size'].sum()
work_order_most_data = total_file_sizes.idxmax()
print(work_order_most_data)


print("\n3) Work package with shortest avarage time between start and competion: ")
df['created'] = pd.to_datetime(df['created'])
df['completed'] = pd.to_datetime(df['status_last_modified'].apply(lambda x: x.get('completed')))

df['duration'] = (df['completed'] - df['created']).dt.total_seconds()
average_durations = df.groupby('work_package')['duration'].mean()
min_duration_package = average_durations.idxmin()
print(min_duration_package)