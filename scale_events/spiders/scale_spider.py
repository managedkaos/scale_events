import scrapy
from scale_events.items import ScaleEventItem


class ScaleScheduleSpider(scrapy.Spider):
    name = "scale_schedule"
    allowed_domains = ["socallinuxexpo.org"]
    start_urls = [
        "https://www.socallinuxexpo.org/scale/22x/schedule/thursday",
        "https://www.socallinuxexpo.org/scale/22x/schedule/friday",
        "https://www.socallinuxexpo.org/scale/22x/schedule/saturday",
        "https://www.socallinuxexpo.org/scale/22x/schedule/sunday",
    ]

    def parse(self, response):
        """First pass: Scrape event list for speaker, title, and URL."""
        for event in response.xpath('//div[contains(@class, "calendar-")]'):
            speaker = event.xpath(
                './/div[contains(@class, "views-field-nothing")]//a/text()'
            ).get()
            title = event.xpath(
                './/div[contains(@class, "views-field-title")]//a/text()'
            ).get()
            url = event.xpath(
                './/div[contains(@class, "views-field-title")]//a/@href'
            ).get()

            if title and speaker and url:
                # Build absolute URL and pass data to the next function
                event_item = ScaleEventItem(
                    speaker=speaker.strip(),
                    title=title.strip(),
                    url=response.urljoin(url),  # Convert to full URL
                )

                yield response.follow(
                    url, self.parse_event_details, meta={"item": event_item}
                )

    def parse_event_details(self, response):
        """Second pass: Follow event page to get time, room, and other details."""
        item = response.meta["item"]

        # Extract event details
        item["day"] = response.xpath(
            '//div[contains(@class, "views-field-field-time")]//span[@class="date-display-single"]/text()'
        ).get()
        item["time"] = response.xpath(
            '//div[contains(@class, "views-field-field-time")]//span[@class="date-display-start"]/text()'
        ).get()
        item["room"] = response.xpath(
            '//div[contains(@class, "views-field-field-room")]//div[@class="field-content"]/text()'
        ).get()
        item["topic"] = response.xpath(
            '//div[contains(@class, "field-content terms")]/a/text()'
        ).get()

        yield item
