import requests
import pandas as pd
import datetime
import dateutil
import json
from datetime import timedelta


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

# Get the dates for the sched_url
today = datetime.datetime.today()
lastWeek = today - timedelta(7)

# Create URL variables for simpler readability when calling
base_url = "https://api.rankonesport.com/PartnerAPI"
sched_url = f"/ScheduleUpdates/?ModifiedDateStart={lastWeek.strftime('%Y%m%d')} 00:00:00&ModifiedDateEnd={today.strftime('%Y%m%d')} 00:00:00"

new = base_url + sched_url
sched_response = requests.get(new, data=credentials["credentials"], headers=headers)
print(sched_response)

# Convert response to JSON
data = sched_response.json()

# Add the content to a Pandas DataFrame
out = pd.DataFrame(data)

# Filter the column for dates that occured at least 1 month out
monthFix = dateutil.relativedelta.relativedelta(months=1)
newDate = today - monthFix
# The 'OUT' will be used for both the scoring and scheduleChange functions
out = out[pd.to_datetime(out["StartDate"]) >= newDate]
out.to_csv("test.csv", index=False)


def scheduleChanges():
    # Modify Dataframe for legibility
    out["StartDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")
    out["EndDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")
    out["DateModified"] = pd.to_datetime(out["DateModified"]).dt.strftime("%m-%d-%Y")

    # Filter out columns we need for schedule change requests
    schedule_Change = out[
        [
            "SportName",
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
            "CombinedScore",
            "GameType",
        ]
    ]

    # Output the file without index
    schedule_Change.to_csv("ScheduleChanges.csv", index=False)


def scoreUpdates():
    """This function will be used to filter out the rows that include a score onlye. Any
    blank rows will be left out."""

    # Call a new dataframe called scores based off the "out" dataframe
    scores = out
    # Filter the scores df to remove blank rows
    scores = scores[scores["CombinedScore"].str.len() > 0]

    # Filter the columns needed
    scoreUpdate = scores[
        [
            "SportName",
            "LevelName",
            "StartDate",
            "EndDate",
            "FacilityName",
            "Address",
            "City",
            "State",
            "Zip",
            "ScheduleDescription",
            "GameStatus",
            "CombinedScore",
            "GameType",
        ]
    ]

    scoreUpdate.to_csv("ScoreChanges.csv", index=False)


# Call the functions as needed
scheduleChanges()
scoreUpdates()
