# CrunchBase API
An API library to download and present organization and people data from CrunchBase based on RapidAPI.
## Quick Start
As shown in the testcase.py file, you can easily retrieve data using cbapi.get_data function.
Input a dictionary of searching parameters and a bool variable. True for organizations and False for people.

```
import cbapi
result_org = cbapi.get_data(name='Tech',locations='New York', True)
result_people = cbapi.get_data(name='Nick',locations='New York', False)  

```
You can also transform the timestamp data retrieved from database into standard format.
```
result_mod = cbapi.change_timestamp(result_org)
```

## Installation

You can use pip to install this package:
```
pip install git+https://github.com/jly1116/cbapi.git
```

## Requirements
The packages needed are:
json
requests
pandas
threading
queue
datetime

## Note and Feedback
 This is finished as a final project of python class in summer semester.
 Please comment for anything you noticed
