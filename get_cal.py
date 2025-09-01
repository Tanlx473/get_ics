'''
Generate an .ics file for the provided weekly timetable (HK timezone + 10-min reminder)
'''
from datetime import datetime, UTC
from uuid import uuid4

# Format to iCalendar local datetime (no 'Z')
def ical_dt(dt: datetime) -> str:
    # UTC 的时间用 Z 结尾（例如 DTSTAMP）
    if dt.tzinfo is UTC:
        return dt.strftime("%Y%m%dT%H%M%SZ")
    # 本地时间（带 TZID 的 DTSTART/DTEND）不带 Z
    return dt.strftime("%Y%m%dT%H%M%S")


def ical_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")

# Base week: assume year 2025, dates shown Mon Sep 1 - Sun Sep 7
year = 2025
TZID = "Asia/Hong_Kong"   # Timezone
WEEKS = 13

events = [
    # Monday Sep 1
    {"summary": "CS 2115 Lecture", "start": datetime(year, 9, 1, 8, 30), "end": datetime(year, 9, 1, 11, 20), "location": "Lecture Theater AC5-315"},
    {"summary": "CS 2115 Tutorial", "start": datetime(year, 9, 1, 11, 30), "end": datetime(year, 9, 1, 12, 20), "location": "Computer Lab AC1-201"},
    {"summary": "CS 2611 Seminar", "start": datetime(year, 9, 1, 14, 0), "end": datetime(year, 9, 1, 16, 50), "location": "Lecture Theater AC5-315"},
    {"summary": "GE 2410 Lecture", "start": datetime(year, 9, 1, 18, 30), "end": datetime(year, 9, 1, 21, 20), "location": "Classroom AC3-215"},

    # Tuesday Sep 2
    {"summary": "CS 2310 Lecture", "start": datetime(year, 9, 2, 8, 30), "end": datetime(year, 9, 2, 11, 20), "location": "Lecture Theater AC5-315"},
    {"summary": "CS 2310 Laboratory", "start": datetime(year, 9, 2, 11, 30), "end": datetime(year, 9, 2, 12, 20), "location": "Computer Lab AC1-201"},
    {"summary": "PE 2911 Lecture", "start": datetime(year, 9, 2, 19, 0), "end": datetime(year, 9, 2, 20, 50), "location": "Outdoor Sports Yard OSY1"},

    # Wednesday Sep 3
    {"summary": "CS 3201 Lecture", "start": datetime(year, 9, 3, 8, 30), "end": datetime(year, 9, 3, 11, 20), "location": "Lecture Theater AC5-315"},
    {"summary": "CS 3201 Tutorial", "start": datetime(year, 9, 3, 11, 30), "end": datetime(year, 9, 3, 12, 20), "location": "Lecture Theater AC5-315"},
    {"summary": "CHEM 1200 Lecture", "start": datetime(year, 9, 3, 14, 0), "end": datetime(year, 9, 3, 16, 50), "location": "Classroom AC5-411"},
    {"summary": "IP 1901 Lecture", "start": datetime(year, 9, 3, 18, 30), "end": datetime(year, 9, 3, 21, 20), "location": "Multi-function Hall AC5-515"},

    # Thursday Sep 4
    {"summary": "MA 2181 Lecture", "start": datetime(year, 9, 4, 8, 30), "end": datetime(year, 9, 4, 11, 20), "location": "Lecture Theater AC5-411"},
    {"summary": "CB 2300 Lecture", "start": datetime(year, 9, 4, 14, 0), "end": datetime(year, 9, 4, 16, 50), "location": "Lecture Theater AC5-416"},

    # Friday Sep 5
    {"summary": "MA 2185 Lecture", "start": datetime(year, 9, 5, 8, 30), "end": datetime(year, 9, 5, 11, 20), "location": "Lecture Theater AC5-315"},
    {"summary": "IP 1902 Lecture", "start": datetime(year, 9, 5, 18, 30), "end": datetime(year, 9, 5, 21, 20), "location": "Multi-function Hall AC5-515"},
]

lines = []
lines.append("BEGIN:VCALENDAR")
lines.append("VERSION:2.0")
lines.append("PRODID:-//Tanlx473//CityUHK(DG) Timetable Export//EN")
lines.append("CALSCALE:GREGORIAN")
lines.append("METHOD:PUBLISH")
lines.append("X-WR-CALNAME:Semester A 2025 Timetable")
lines.append(f"X-WR-TIMEZONE:{TZID}")

# VTIMEZONE for Asia/Hong_Kong (no DST)
lines.append("BEGIN:VTIMEZONE")
lines.append(f"TZID:{TZID}")
lines.append("X-LIC-LOCATION:Asia/Hong_Kong")
lines.append("BEGIN:STANDARD")
lines.append("TZOFFSETFROM:+0800")
lines.append("TZOFFSETTO:+0800")
lines.append("TZNAME:HKT")
lines.append("DTSTART:19700101T000000")
lines.append("END:STANDARD")
lines.append("END:VTIMEZONE")

rrule = f"RRULE:FREQ=WEEKLY;COUNT={WEEKS}"

for e in events:
    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{uuid4()}@timetable.local")
    lines.append(f"DTSTAMP:{ical_dt(datetime.now(UTC))}")
    lines.append(f"SUMMARY:{ical_escape(e['summary'])}")
    # Hong Kong Timezone
    lines.append(f"DTSTART;TZID={TZID}:{ical_dt(e['start'])}")
    lines.append(f"DTEND;TZID={TZID}:{ical_dt(e['end'])}")
    lines.append(f"LOCATION:{ical_escape(e['location'])}")
    lines.append(rrule)

    #  10 min before remind
    lines.append("BEGIN:VALARM")
    lines.append("ACTION:DISPLAY")
    lines.append("DESCRIPTION:Reminder")
    lines.append("TRIGGER:-PT10M")
    lines.append("END:VALARM")

    lines.append("END:VEVENT")

lines.append("END:VCALENDAR")

ics_path = "weekly_timetable_2025_semester.ics"
with open(ics_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Saved to {ics_path}")
