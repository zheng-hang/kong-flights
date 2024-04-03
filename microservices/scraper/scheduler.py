import schedule

# import schedule
import time
from invokes import invoke_http

# Run scheduler

def scrapeAPI():
    results = invoke_http('http://127.0.0.1:5104/scrapeAPIs', method='GET')
    return results

# Schedule the job to run at midnight
schedule.every().day.at("00:00").do(scrapeAPI())

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)