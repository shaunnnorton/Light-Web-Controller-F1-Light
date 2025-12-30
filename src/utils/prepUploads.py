import json
import pandas as pd
from datetime import datetime as dt
from .. import config

def parseUploadedExcel(filename):

    try:
        export_json = {}
        uploadedDF = pd.read_excel(filename,engine="openpyxl").to_dict(orient="index")
        for row in uploadedDF:
            export_json[row["Date"]] = {
                "Track Name": row["Track Name"],
                "RaceNumber": row["Race Number"]
            }
        
        with open(f"./src/static/schedules/ImportedSchedule{dt.now().strftime("%Y%m%d%H%M%s")}.json", "w") as newfile:
            newfile.write(json.dumps(export_json))
            new_filename = newfile.name

        appconfig = config.Config()

        with open(config.currentScheduleFile,"rw") as config_file:
            config_json = json.load(json)
            config_json.currentScheduleFile = new_filename
            config_file.write(json.dump(config_json))

        return "File successfully uploaded!"
    except Exception as e:
        return f"Error when uploading file. Please check format and try again. \n EXCEPTION {e}"