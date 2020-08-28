import json
import requests
import pandas as pd
from threading import Thread
from queue import Queue
from datetime import datetime, timedelta

RAPIDAPI_KEY = ""
# enter your own RapidAPI key, register on rapidapi.com to get one in case you don't

def get_api_key():
    return RAPIDAPI_KEY

def trigger_api(search_params:dict, is_org:bool):
    # trigger api to get date from rapidapi
    user_apikey = get_api_key()
    headers = {
      'x-rapidapi-host': "crunchbase-crunchbase-v1.p.rapidapi.com",
      'x-rapidapi-key': user_apikey
     }
    if is_org:
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-organizations"
    else:
        url = "https://crunchbase-crunchbase-v1.p.rapidapi.com/odm-people"

    response = requests.request("GET", url, headers=headers, params=search_params)
    if(200 == response.status_code):
        return json.loads(response.text)
    else:
        return None

def get_data(search_params:dict, is_org:bool):
    '''
    :param search_params: a dictionary for searching
    for organizations, we accept:
    updated_since: (int) restricts to Organizations where updated_at >= the passed value, should input timestamp
    query: (string) Full text search of an Organization's name, aliases
    name: (string) Full text search limited to name and aliases
    domain_name: (string) Text search of an Organization's domain_name
    locations: (string) Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco
    organization_types: (string) Filter by one or more types. Available types are "company", "investor", "school", and "group"
    sort_order: (string) Options are "createdat ASC", "createdat DESC", "updatedat ASC", and "updatedat DESC"
    page: (int) Page number of the results to retrieve

    for people, we accept:
    name: (string) A full-text query of name only
    query: (string) A full-text query of name, title, and company
    updated_since: (int) restricts to People where updated_at >= the passed value, should input timestamp
    sort_order: (string) Options are "createdat ASC", "createdat DESC", "updatedat ASC", and "updatedat DESC"
    page: (int) Page number of the results to retrieve
    locations: (string) Filter by location names (comma separated, AND'd together) e.g. locations=California,San Francisco
    socials: (string) Filter by social media identity (comma separated, AND'd together) e.g. socials=ronconway
    types: (string) Filter by type (currently, either this is empty, or is simply "investor")

    :param is_org: (Boolean) whether we want to get organization data(use True) or people data(use False)
    :return: pandas.DataFrame
    '''

    raw_data = trigger_api(search_params,is_org)
    num_pages = raw_data['data']['paging']['number_of_pages']
    df = pd.DataFrame(list(pd.DataFrame(raw_data['data']['items'])['properties']))
    current_page = raw_data['data']['paging']['current_page']
    threads=[]
    q=Queue()

    if current_page!=1:
        return df

    def add_one_page(queue, search_params, is_org):
        queue.put(get_data(search_params, is_org))

    if num_pages<=1:
        return df
    else:
        # if more than 1 pages, use multithreading to speed up
        for thread_count in range(num_pages-1):
            params_temp = search_params.copy()
            params_temp['page'] = thread_count+2           # change or add the key and value
            threads.append(Thread(target=add_one_page, args=(q, params_temp, is_org)))      # use thread for each page
            threads[thread_count].start()
        for thread_count in range(len(threads)):
            threads[thread_count].join()
            df = df.append(q.get(), ignore_index=True)
    return df

def timestamp_to_datetime(timestamp:int):
    # converts UNIX timestamp to datetime project, local time is standard time in China
    if isinstance(timestamp, (int,float)):
        dt = datetime.utcfromtimestamp(timestamp) + timedelta(hours=8)
    return dt

def change_timestamp(df:pd.DataFrame):
    # change the timestamp in dataframe to more readable format, yyyy-mm-dd hour:minute:second
    df['created_at'] = df['created_at'].apply(timestamp_to_datetime)
    df['updated_at'] = df['updated_at'].apply(timestamp_to_datetime)
    return df

if __name__ == "__main__":
    condition = {'name': 'Nick', "locations": "New York"}
    condition_org = {'name': 'Data',"locations": 'California'}
    result = get_data(condition_org, False)
    result_mod = change_timestamp(result)
    print(result_mod)





