import requests
import pandas as pd
import datetime
import dateutil
import json


# Load credentials from JSON File
file = open("Credentials.json")
data = json.load

# Initialize Variables
url = "https://api.rankonesport.com/PartnerAPI/Auth/ValidateUser"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "",
}
headers["Authorization"] = data["headers"]["Authorization"]

response = requests.post(url, data=data, headers=headers, json={"key": "value"})
print(response)

headers["Authorization"] = "bearer " + response.json()["access_token"]
headers["Content-Type"] = "application/json"

base_url = "https://api.rankonesport.com/PartnerAPI"
sched_url = "/ScheduleUpdates/?ModifiedDateStart=20220201 00:00:00&ModifiedDateEnd=20220223 00:00:00"

new = base_url + sched_url
sched_response = requests.get(new, data=data, headers=headers)
data = sched_response.json()

out = pd.DataFrame(data)

# Filter for date only
today = datetime.datetime.today()
monthFix = dateutil.relativedelta.relativedelta(months=1)
newDate = today - monthFix
out = out[pd.to_datetime(out["StartDate"]) >= newDate]
out.to_csv("schedule-update.csv", index=False)

# Modify Dataframe
out["StartDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")
out["EndDate"] = pd.to_datetime(out["StartDate"]).dt.strftime("%m-%d-%Y %I:%M%p")

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

schedule_Change.to_csv("newtest.csv", index=False)
