import json
import pandas as pd
from datetime import datetime as dt
from .. import config

def parseUploadedExcel(filename):

    # try:
    export_json = {}
    uploadedDF = pd.read_excel(filename,engine="openpyxl").to_dict(orient="index")
    for row in uploadedDF:
        #print(type(uploadedDF[row]["Date"]))
        export_json[uploadedDF[row]["Date"].strftime("%-m/%-d/%Y")] = {
            "Track Name": uploadedDF[row]["Track Name"],
            "RaceNumber": uploadedDF[row]["Race Number"]
        }
    
    with open(f"./src/static/schedules/ImportedSchedule{dt.now().strftime("%Y%m%d%H%M%s")}.json", "w") as newfile:
        newfile.write(json.dumps(export_json))
        new_filename = newfile.name


    with open("attributes.json","r") as config_file:
        print(config_file)
        config_json = json.loads(config_file.read())
        config_json.currentScheduleFile = "./src/static/schedules/"+new_filename
        
    with open("attributes.json","w") as config_file_new:
        print(config_json)

        config_file_new.write(json.dumps(config_json))

    return "File successfully uploaded!"
    # except Exception as e:
    #     return f"Error when uploading file. Please check format and try again. \n EXCEPTION {e}"