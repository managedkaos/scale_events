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
import os

# Define the order of days
DAYS = ["Thursday", "Friday", "Saturday", "Sunday"]

if __name__ == "__main__":
    # Load the data coming in
    events = bios.read("events.json")

    # Prep for the data going out
    events_csv = [["Day", "Time", "Title", "Speaker", "URL", "Room", "Topic"]]
    sorted_events = []

    print("# SCaLE 22x Schedule\n")

    for day in DAYS:
        print(f"## {day}\n")

        # Get all events for the day
        events_by_day = [e for e in events if "22x" in e.get("url") and e.get("day") and e.get("day").split(",")[0] == day]

        # Sort events by time before processing
        events_by_day.sort(key=lambda x: x.get("time", ""))

        for event in events_by_day:
            date = event.get("day").split(",")[1].strip()
            time = event.get("time")
            room = event.get("room")
            speaker = event.get("speaker").replace('"', '')
            title = event.get("title")
            url = event.get("url")
            topic = event.get("topic")

            sorted_events.append({
                "day": day,
                "time": time,
                "room": room,
                "speaker": speaker,
                "title": title,
                "url": url,
                "topic": topic
            })

            events_csv.append([day,time,title,speaker,url,room,topic])

            print(f"- [{title}]({url})")
            print(f"  - {speaker}")
            print(f"  - {time} - {room}")
            print()

    # Create the './public' directory if it doesn't exist
    os.makedirs("public", exist_ok=True)

    bios.write("./public/sorted_events.json", sorted_events)
    with open('./public/events.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for event in events_csv:
            writer.writerow(event)
