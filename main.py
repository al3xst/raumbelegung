from flask import Flask, json, render_template
from icalendar import Calendar, Event
import urllib
from datetime import datetime

import pytz

app = Flask(__name__)

# rooms we are interested in:

# Seminarraum 00.200 (0. floor)
# Seminarraum 01 (2. floor)
# Seminarraum 02 (2. floor)
# Seminarraum 03
# Seminarraum 04
# Seminarraum 05
# Seminarraum 06
# Seminarraum 07
# Seminarraum 08
# Seminarraum 09 (4. floor)
# Seminarraum 10
# Seminarraum 11
# Seminarraum 12
# Seminarraum Statistik 2/104 (2. floor)
# Hörsaal (0. floor)
# Seminarraum A (0. floor)
# Seminarraum B (0. floor)
# Seminarraum C (0. floor)
# Common Room (5. floor)
# Konferenzraum (5. floor)
# PC-Pool Software 1 (3. floor)
# PC-Pool Software 2 (3. floor)

entries = []
rooms = ["Seminarraum 00.200",
         "Seminarraum 01",
         "Seminarraum 02",
         "Seminarraum 03",
         "Seminarraum 04",
         "Seminarraum 05",
         "Seminarraum 06",
         "Seminarraum 07",
         "Seminarraum 08",
         "Seminarraum 09",
         "Seminarraum 10",
         "Seminarraum 11",
         "Seminarraum 12",
         "Seminarraum Statistik 2/104",
         "Hörsaal",
         "Seminarraum A",
         "Seminarraum B",
         "Seminarraum C",
         "Common Room",
         "Konferenzraum",
         "PC-Pool Software 1",
         "PC-Pool Software 2"]

matrix = [["<td bgcolor=#00e64d></td>"]*14 for i in range(len(rooms)+1)]

for i in range(1, 14):
    matrix[0][i] = "<th>" + str(8+i) + "</th>"

for i in range(1, len(matrix)):
    matrix[i][0] = "<td><b>" + rooms[i-1] + "</b></td>"


# 9 Uhr Sr 01: Matrix[1][1]
# 11 Uhr Sr 01: Matrix[1][3]

@app.route("/")
def main():
    htmltable = ""

    for row in matrix:
        htmltable += "<tr>"
        for cell in row:
            htmltable += cell
        htmltable += "</tr>"

    return render_template("index.html", tablecontent=htmltable)


def regenEntries():
    file = open("ical.ics", "rb")
    cal = Calendar.from_ical(file.read())

    tz = pytz.timezone('Europe/Berlin')
    today = datetime.now(tz)

    entries = [dict(summary=str(event['SUMMARY']), location=str(event['LOCATION']), begin=event['DTSTART'].dt.hour + 2,
                    end=event['DTEND'].dt.hour + 2)
               for event in cal.walk('VEVENT')
               if (event['DTSTART'].dt.day == today.day == event['DTEND'].dt.day)
               and (event['DTSTART'].dt.month == today.month == event['DTEND'].dt.month)
               and (event['DTSTART'].dt.year == today.year == event['DTEND'].dt.year)]
    # json.dumps(entries, indent=2, sort_keys=True)

    # print(entries)

    for i in range(len(rooms) - 1):
        for event in entries:
            if event["location"] == rooms[i] and event["begin"] > 7:
                matrix[i + 1][event["begin"] - 8] = "<td colspan=" + str(event["end"] - event["begin"]) + ">" + event[
                    "summary"] + "</td>"
                for j in range(0, (event["end"] - event["begin"] - 1)):
                    matrix[i + 1][event["begin"] - 8 + j + 1] = ""

                    # print(matrix)


from threading import Timer


def job_function():
    Timer(60*60, job_function).start()
    print("Regnerated entries")
    regenEntries()


if __name__ == "__main__":

    job_function()

    app.run(port=5001)