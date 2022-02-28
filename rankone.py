import requests
import pandas as pd
import datetime
import dateutil
import json


# Load credentials from JSON File
file = open("Credentials.json")
credentials = json.load(file)

# Initialize Variables
url = "https://api.rankonesport.com/PartnerAPI/Auth/ValidateUser"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "",
}

# Define auth code from the JSON file
headers["Authorization"] = credentials["headers"]["Authorization"]

# Use POST to acquire the bearer token
response = requests.post(
    url, data=credentials["credentials"], headers=headers, json={"key": "value"}
)
print(response)

# Reassign the auth and content type to the new bearer token and JSON content-type
headers["Authorization"] = "bearer " + response.json()["access_token"]
headers["Content-Type"] = "application/json"

# TODO: Add date formatting to schedURL
base_url = "https://api.rankonesport.com/PartnerAPI"
sched_url = "/ScheduleUpdates/?ModifiedDateStart=20220201 00:00:00&ModifiedDateEnd=20220223 00:00:00"

new = base_url + sched_url
sched_response = requests.get(new, data=credentials["credentials"], headers=headers)
print(sched_response)

# Convert response to JSON
data = sched_response.json()

# Add the content to a Pandas DataFrame
out = pd.DataFrame(data)

# TODO: Move the variables above base and sched URL
# Filter for date only
today = datetime.datetime.today()
monthFix = dateutil.relativedelta.relativedelta(months=1)
newDate = today - monthFix
out = out[pd.to_datetime(out["StartDate"]) >= newDate]
out.to_csv("schedule-update.csv", index=False)

# TODO: Add filtering and column selections to it's own function
# Modify Dataframe for legibility
out["StartDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")
out["EndDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")

# Filter out columns we need for schedule change requests
schedule_Change = out[
    [
        "SportName",
        "SportGender",
        "LevelName",
        "StartDate",
        "EndDate",
        "DateModified",
        "FacilityName",
        "Address",
        "City",
        "State",
        "Zip",
        "ScheduleDescription",
        "GameStatus",
    ]
]

# Output the file without index
schedule_Change.to_csv("newtest.csv", index=False)

# TODO: add a function for filtering based on added game scores
