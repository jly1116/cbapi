import cbapi

if __name__ == "__main__":
    search_org = {'name': 'Tech',"locations": 'New York'}
    search_people = {'name': 'Nick', "locations": "New York"}
    result_org = cbapi.get_data(search_org, True)           # retrieve organization data
    result_people = cbapi.get_data(search_people, False)    # retrieve people data
    result_mod = cbapi.change_timestamp(result_org)         # change timestamp to local standard time
