from dotenv import load_dotenv
import os
import requests
import json
from twilio.rest import Client

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
ayush_number = os.environ['AYUSH_NUMBER']
shradha_number = os.environ['SHRADHA_NUMBER']
sai_number = os.environ['SAI_NUMBER']

def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)
 
def print_time_and_date():   
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.date()
    data = "Checked at: Current Time = {}, Date = {}".format(current_time, current_date)
    return data

def check_people_to_send_message(course_code, course_name, people):
    if 'ayush' in people:
        send_text(course_code, course_name, ayush_number)
    if 'sai' in people:
        send_text(course_code, course_name, sai_number)
    if 'shradha' in people:
        send_text(course_code, course_name, shradha_number)

def send_text(course_code, course_name, number):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                            body="Course {} Index {} is open! Sign up at \nhttps://sims.rutgers.edu/webreg/chooseSemester.htm?login=cas".format(course_name, course_code),
                            from_=twilio_number,
                            to=number
                        )
    except Exception as e:
        write_file('logs.txt' , type(e).__name__ + ": " + e.__str__())
        raise SystemExit(e)

url = 'https://sis.rutgers.edu/soc/api/openSections.json'

params = dict(
    year='2022',
    term='9',
    campus='NB'
)

try:
    resp = requests.get(url=url, params=params)
    data = resp.json()
    courses = json.load(open('courses.json', 'r'))
except Exception as e:  # This is the correct syntax
    write_file('logs.txt' , type(e).__name__ + ": " + e.__str__())
    raise SystemExit(e)



for course_code in data:
    if(courses.__contains__(course_code)):
        check_people_to_send_message(course_code, courses[course_code]['name'], courses[course_code]['people'])
        courses[course_code]['count'] = courses[course_code]['count'] - 1
        if(courses[course_code]['count'] == 0):
            courses.pop(course_code, None)

json.dump(courses, open('courses.json', 'w'))

from datetime import datetime
import os
 
write_file('logs.txt' , print_time_and_date())
