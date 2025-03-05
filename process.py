import bios

# Define the order of days
DAYS = ["Thursday", "Friday", "Saturday", "Sunday"]

# Event Format
# {"day": "Saturday", "time": null, "room": null, "speaker": "Autumn Nash", "title": "Barbie's Journey: A CI/CD Tale of Transformation", "url": "https://www.socallinuxexpo.org/scale/22x/presentations/barbies-journey-cicd-tale-transformation"}

if __name__ == "__main__":
    # Load scraped event data
    events = bios.read("events.json")
    events_with_no_day = []

    print("# SCaLE 22x Schedule\n")

    for day in DAYS:
        print(f"## {day}\n")

        for event in events:
            if event.get("day"):
                day_of_the_week = event.get("day").split(",")[0]
                print(day_of_the_week)
            else:
                events_with_no_day.append(event)
                continue
