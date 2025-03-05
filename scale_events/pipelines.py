import json


class ScaleEventsPipeline:
    def open_spider(self, spider):
        self.events = []

    def process_item(self, item, spider):
        self.events.append(dict(item))
        return item

    def close_spider(self, spider):
        # Sort events by day, room, and time
        self.events.sort(key=lambda x: (x["day"], x["room"], x["time"]))

        # Save as JSON file
        with open("sorted_scale_events.json", "w") as f:
            json.dump(self.events, f, indent=4)
