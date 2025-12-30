from src import app
import threading
from src.utils import cal


if __name__ == "__main__":

    schedule = cal.Schedule(".src/static/schedules/testSchedule.json")
    background_thread = threading.Thread(target=schedule.functionalLoop)
    server_thread = threading.Thread(target=app.run, kwargs={"debug":False,"port":8080, "host":"0.0.0.0"})
    #app.run(debug=False,port=8080, host="0.0.0.0")
    background_thread.start()
    server_thread.start()