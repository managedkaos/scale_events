"""
This script processes the scraped event data and outputs a markdown file with the schedule.

The scraped data has the format:

{
    "speaker": "Autumn Nash",
    "title": "Barbie's Journey: A CI/CD Tale of Transformation",
    "url": "https://www.socallinuxexpo.org/scale/22x/presentations/barbies-journey-cicd-tale-transformation",
    "day": "Saturday, March 8, 2025 - ",
    "time": "18:15",
    "room": "Room 211",
    "topic": "Developer"
}
"""
import bios
import csv

# Define the order of days
DAYS = ["Thursday", "Friday", "Saturday", "Sunday"]

if __name__ == "__main__":
    # Load scraped event data
    events = bios.read("events.json")
    events_csv = [["Day", "Time", "Title", "Speaker", "URL", "Room", "Topic"]]

    print("# SCaLE 22x Schedule\n")

    for day in DAYS:
        print(f"## {day}\n")

        # Sort events by time before processing
        events_for_day = [e for e in events if "22x" in e.get("url") and e.get("day") and e.get("day").split(",")[0] == day]

        events_for_day.sort(key=lambda x: x.get("time", ""))

        for event in events_for_day:
            time = event.get("time")
            room = event.get("room")
            speaker = event.get("speaker")
            title = event.get("title")
            url = event.get("url")
            topic = event.get("topic")

            events_csv.append([day,time,title,speaker,url,room,topic])

            print(f"- [{title}]({url})")
            print(f"  - {speaker}")
            print(f"  - {time} - {room}")
            print()

    with open('events.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for event in events_csv:
            writer.writerow(event)
