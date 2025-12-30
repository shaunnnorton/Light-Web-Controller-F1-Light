import threading
import json
from datetime import datetime as dt
from time import sleep
from requests import request
from math import ceil
from .. import config

# Date
## Track Name
## Race Number


class Schedule():
    current_schedule = {}
    next_date = dt(2000,1,1)
    current_time = None
    appconfig = None

    def __init__(self, startingSchedulePath):
        try:
            with open(startingSchedulePath) as startingFile:
                self.current_schedule = json.load(startingFile)
            self.current_time = dt.now()
            self.findNextDate()
            self.appconfig = config.Config()
        except:
            self.appconfig = config.Config()
            self.current_schedule = {}
            self.next_date = dt(2000,1,1)
            self.current_time = dt.now()
        


    def findNextDate(self):
        print(
            self.appconfig,
            self.current_schedule,
            self.next_date,
            self.current_time)
        self.current_time = dt.now()
        for date in self.current_schedule.keys():
            parsedDate = dt.strptime(date, "%m/%d/%Y")
            if parsedDate.date() >= self.current_time.date() and parsedDate.date() <= self.next_date.date():
                self.next_date = parsedDate
        return self.next_date


    def lightCurrentTrack(self):
        track_number = self.current_schedule[self.current_time]["RaceNumber"]
        row = ceil(track_number/6)
        column = track_number % 6 if track_number % 6 != 0 else 6

        print(f'Track: {self.current_schedule[self.current_time]["RaceNumber"]} Row:{row} Column: {column}')

        request("GET",f"https://localhost:8080/Automatic", params={"row":row, "column":column})


    def refreshSchedule(self):
        self.appconfig.get_updated_attributes()
        with open(self.appconfig.currentScheduleFile, "r") as newfile:
            self.current_schedule = json.load(newfile)


    def functionalLoop(self):

        while True:
            sleep(60)
            self.refreshSchedule()
            self.findNextDate()
            if self.current_time.date() == self.next_date.date():
                print(f"Updating Track: {self.current_schedule[self.next_date]["Track Name"]}")
                self.lightCurrentTrack()


    


