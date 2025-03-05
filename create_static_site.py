"""Compiles the metadata and template into a static HTML file"""

import bios
from jinja2 import Environment, FileSystemLoader

# Define the output directory
PUBLIC_DIRECTORY = "./public"
TEMPLATES_DIRECTORY = "./templates"

# Read data from the JSON file using the 'bios' module
events = bios.read(f"{PUBLIC_DIRECTORY}/sorted_events.json")

# Create a Jinja2 environment with the templates directory
env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY))

# Load the template for event processing
event_template = env.get_template("index.html")

# Render the template with the events; '| tojson' is applied in the template
rendered_template = event_template.render(events=events)

# Save the rendered template as an HTML file
with open(f"{PUBLIC_DIRECTORY}/index.html", "w", encoding="utf-8") as html_file:
    html_file.write(rendered_template)

print(f"# Template populated and saved as {PUBLIC_DIRECTORY}/index.html")
