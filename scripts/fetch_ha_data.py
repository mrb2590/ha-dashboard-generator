from dotenv import load_dotenv
from rich import print
import json
import os
import requests
import yaml

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
HA_URL = os.getenv("HA_URL")
TOKEN = os.getenv("HA_TOKEN")
# ---------------------

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# Read the Jinja template from the file
print("Reading Jinja template from file...")
with open("queries/get_lights.jinja", "r") as template_file:
    ha_template = template_file.read()

print("Fetching live area and light data from Home Assistant...")

try:
    # Ask Home Assistant to render the template
    response = requests.post(f"{HA_URL}/api/template", headers=headers, json={"template": ha_template})
    response.raise_for_status()
    
    # Parse the returned JSON string into Python dictionaries
    areas_data = json.loads(response.text)
    
    # Wrap it in the top-level "areas:" key to match our makejinja template
    final_data = {"areas": areas_data}
    
    # Ensure the build directory exists
    os.makedirs("build", exist_ok=True)
    
    # Save the data inside the build directory
    with open("build/data.yaml", "w") as f:
        yaml.dump(final_data, f, default_flow_style=False, sort_keys=False)
    
    print("[bold green]Successfully generated data.yaml![/bold green]")

except Exception as e:
    print(f"[bold red]Error fetching data:[/bold red]\n[red]{e}[/red]")