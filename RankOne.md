# RankOne Python Script / API call

This document will provide the information for the API call and subsequent python script.

## Authentication
In order to pull information using the rankone API, the following parameters have to be added to the call in order to retrieve information. *Note:* This could change so update accordingly. For security reasons, this will not be added to the main script for GIT changes. Please contact someone in office for the credentials.

* **Username**
* **Password**
* **API Key**

## Pre-Reqs
Before running the script, we will need to have python3.8+ installed, along with the following packages.

```python
import requests
import pandas as pd
import datetime
import dateutil
```

## Process

The first step is to authenticate the session by calling the API key as a *Basic* authorization header, and setting the 'content-type' as "application/x-www-form-urlencoded".
This response will be called using **POST**, and will return a temporary authentication token for us to use. The URL for this call is <https://api.rankonesport.com/PartnerAPI/Auth/ValidateUser>

*Sample Authentication Script:*

```python
# Data dict to call on the username and password during authentication
data = {"Username": "", "Password": ""}

# This URL never changes (Unless RankOne changes their API)
url = "https://api.rankonesport.com/PartnerAPI/Auth/ValidateUser"

# The headers dict to hold the content type and auth token/API key
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "",
}

# Here we set the json to key/value in order to parse the auth key later
response = requests.post(url, data=data, headers=headers, json={"key": "value"})
```

If the first call is successful, we use the returned auth-key as our new *Bearer* token, and set the 'content-type' to "application/json".  The base URL for this is <https://api.rankonesport.com/PartnerAPI>. Any specific reference will simply be added to this base URL. This response will be called using **GET**.

*Sample Code*

```python
# Instead of using a new dict, we simply modify our current headers dict with our new access token and content type
headers["Authorization"] = "bearer " + response.json()["access_token"]
headers["Content-Type"] = "application/json"

# This base URL does not change
baseURL = "https://api.rankonesport.com/PartnerAPI"

# The callURL will be any data you are trying to pull
callURL = "{CHANGE URL HERE}"

# Here, we combine our URLs into one, and call it using requests.
new = baseURL + callURL
sched_response = requests.get(new, data=data, headers=headers)

# The response is converted to JSON, for ease of use when converting to a pandas dataframe
data = sched_response.json()
```

## Schedule Updates
This section will go over how to pull any schedule updates. The official RankOne documentation on this call can be found here: 

<https://rankone.com/apidocumentation/districtapi/dgetscheduleupdates.aspx>

The only required fields are "ModifiedDateStart" and "ModifiedDateEnd". Please note that these fields only indicate when a schedule was changed, **NOT** that the game is in the current or near future.
One example is that a coach added scores to a game that happened last year. This would trigger the game to show up on our report due to it being modified within our timeframe. 

There are a lot of columns that show up in the raw data. After review, only a few of them are necessary for this particular report run.  To pull the exact columns needed, we have to filter. This will be covered in a different section.

*EXAMPLE:*

```python
# First, we need to set our current date to today when the script is run
today = datetime.datetime.today()

# If the script is run weekly, we simply subtract 7 days and call it new_date
prior = datetime.timedelta(7)
newDate = today - prior

# In order to have the proper format, we simply convert the datetime. The proper format is yyyyMMdd hh:mm:ss
urlToday = pd.to_datetime(today).strftime("%Y%m%d")
urlLastWeek = pd.to_datetime(newDate).strftime("%Y%m%d")

# Now that we have the proper format, simply use an f-string to plug and go. Note that we set the time to 00:00:00 for simplification
scheduleURL = f"/ScheduleUpdates/?ModifiedDateStart={urlLastWeek} 00:00:00&ModifiedDateEnd={urlToday} 00:00:00"

# Our base layer API call should remain unchanged. Simply combine the 2 and call using requests. You optionally could print the request to ensure a [200] is returned.
newURL = baseURL + scheduleURL
scheduleResponse = requests.get(newURL, data=data, headers=headers)

# Add the output as a JSON and add it to a pandas dataframe
data = scheduleResponse.json()
scheduleData = pd.DataFrame(data)
```

## Updated Game Scores
The process of pulling the report will be the same as the schedule change. The only things that we modify are the columns we select. Filtering will be detailed in another section.

## Columns
Here is a table of all the columns and a small description. This will help decide which columns you need when filtering/selecting.

| Column               | Description                                     |
|:-------------------- | ----------------------------------------------- |
| ID                   | ID of the game                                  |
| TeamID               | ID of the team (Softball (M))                   |
| SchoolID             | St. Pius X RankOne internal ID                  |
| SchoolName           | "St. Pius X Catholic School-Houston"            |
| SportName            | Sport with Gender: Baseball (M)                 |
| SportGender          | Gender of the Sport                             |
| LevelName            | Varsity, JV etc                                 |
| TeamName             | "Panthers"                                      |
| StartDate            | When the game starts                            |
| StartDateOffset      | Shows by how much the date was changed          |
| StartTime            | Time when starts. Although this is in StartDate |
| EndDate              | When the game ends                              |
| EndDateOffset        | Shows the difference in change in EndDate       |
| DateModified         | When the schedule was changed                   |
| DateModifiedOffset   | ?                                               |
| StartTBD             | TRUE/FALSE if the StartDate is blank            |
| EndTBD               | TRUE/FALSE if the EndDate is blank              |
| FacilityName         | Name of the facility where the team plays       |
| Address              | Street Address                                  |
| City                 |                                                 |
| State                |                                                 |
| Zip                  |                                                 |
| ScheduleDescription  | How the game is presented online                |
| OpponentTeamName     | This data is included in ScheduleDescription    |
| TeamScore            | Present if reported                             |
| OpponentScore        | Present if reported                             |
| CombinedScore        | Present if reported                             |
| Location             | 'Home'/'Away'                                   |
| LocationSymbol       | 'Vs' / '@'                                      |
| SpecialNotes         | Description footer coach puts in                |
| GameSummary          |                                                 |
| GameType             |                                                 |
| BusArrivalTime       |                                                 |
| BusDepartureTime     |                                                 |
| StudentDismissalTime |                                                 |
| GameNotes            |                                                 |
| Televised            |                                                 |
| MapAddress           | Google Maps link                                |
| GameAttachmentId     |                                                 |
| FileName             |                                                 |
| Facility_ID          |                                                 |
| FacilityAway_ID      |                                                 |
| GameStatus           | 'Scheduled' / 'Cancelled' / 'Deleted'           |
| StreamURL            |                                                 |
| StreamStartDate      |                                                 |

## Filtering and Selection
To filter, we simply need to make a new variable, and add the columns that we need in a list.

*Example:*

```python
# 'data' would be whatever variable we called the panda dataframe
scheduleChange = data[
	[
	 'SportName',
	 'StartDate',
	 'GameStatus',
	]
]

# To Save, simply call our new selection to csv. Set index to false since it isn't needed
scheduleChange.to_csv("NAMEFILEHERE.csv", index=False)
```
## Conclusion
The API documentation doesn't mention anything about token limits, so running it multiple times should pose no issue.
The CSV could be saved into a OneDrive folder, which then gets moved to Sharepoint and emailed to the necessary contacts.