"""
Author: Saba Konjaria
Created at: 19-Jan-2023
Brief:  This program is about to take some information from the user such as a task that he/she
      has done during the day. program analyses input and adds up it to a new rows into
      the spreadsheet as a representation of a new task created by him/her for today and for a moment
"""

import requests
from datetime import datetime
import requests.auth
import os
from threading import Thread

# ------------- Take input from the user --------------------------------------
# Notice that there are not handled exceptions
usr_input = input("What you've done today? Put your exercise right there: ")
gender = input("Your gender: ")
weight = input("Your mass(kg): ")
height = input("Your Height(cm): ")
age = input("How old are you? Your age: ")

# ------------------ Sheety API ----------------------------
sheety_api_endpoint = "https://api.sheety.co/b1a427ad429e8a1dbe011cc7f0bf3571/copyOfMyWorkouts/workout"
password = os.environ.get("SHETY_PASWD")
username = os.environ.get("SHETY_USNM")
basic = requests.auth.HTTPBasicAuth(username=username, password=password)

# ------------------ Nutritionix API ----------------------------
APP_ID = os.environ.get("NUTR_APP_ID")
API_KEY = os.environ.get("NUTR_API_KEY")
ENDPOINT = "https://trackapi.nutritionix.com"
body = {
    "query": usr_input,
    "gender": gender,
    "weight_kg": float(weight),
    "height_cm": float(height),
    "age": int(age)
}
headers = {
    "X-APP-ID": APP_ID,
    "X-APP-KEY": API_KEY,
}

response = requests.post(url=ENDPOINT + "/v2/natural/exercise",
                         json=body,
                         headers=headers)
data = response.json()
for i in range(len(data.get("exercises"))):
    updated_row = {
        "workout": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": data.get("exercises")[i].get("name").title(),
            "duration": str(data.get("exercises")[i].get("duration_min")),
            "calories": str(data.get("exercises")[i].get("nf_calories")),
        }
    }
    sheety_call = requests.post(sheety_api_endpoint, json=updated_row, auth=basic)

    if sheety_call.status_code == 200:
        print("Successfully added to the spreadsheet ✅")
    else:
        print("Oops.... Something went wrong")
