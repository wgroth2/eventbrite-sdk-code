# SDK here: https://github.com/eventbrite/eventbrite-sdk-python
# API Reference: https://www.eventbrite.com/platform/api
#
# Author: Bill.roth@secondfront.com
#
from eventbrite import Eventbrite
import mariadb
import sys

def insert_attendees():

    try:
        eventbrite = Eventbrite('YOURCODE')
    except Exception as e:
        print(e)
        sys.exit(1)

    
#user = eventbrite.get_user()  # Not passing an argument returns yourself
#print(user['id'])
#
#event = eventbrite.get_event('YOUREVENTID')
#print(event['name'])
    attendees = eventbrite.get_event_attendees('YOUREVENTID')
    num_attendees = attendees['pagination']['object_count']
# print(f"Number of attendees: {num_attendees}")

# Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="db_user",
            password="PASSWORD",
            host="yourhost.com",
            port=3306,
            database="yourdb"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    #
    # https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
    #
    try: 
        cur.execute(f"INSERT INTO `metrics` (`ts`, `ID`, `val`, `campaign`) VALUES (current_timestamp(), NULL, '{num_attendees}', 'offset23-registrants');")
    except mariadb.Error as e: 
        print(f"Error: {e}")
        sys.exit(1)
    #
    x=0
    conn.commit()
    conn.close()

def main():
    insert_attendees()

if __name__ == "__main__":
    main()
