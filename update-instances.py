import yaml
import httpx

# Read .uptimerc.yaml config file
with open(".upptimerc.yml", "r", encoding="UTF-8") as f:
    config = yaml.safe_load(f)

# Get the list of instances
resp = httpx.get(
    "https://raw.githubusercontent.com/wiki/TeamPiped/Piped-Frontend/Instances.md")

# Parse the list of instances
instances = []

skipped = 0

for line in resp.text.splitlines():

    split = line.split("|")

    if len(split) < 4:
        continue

    if skipped < 2:
        skipped += 1
        continue

    instances.append({
        "name": split[0].strip(),
        "url": split[1].strip(),
        "locations": split[2].strip(),
    })

# Update the config file
config["sites"] = [{
    "name": x["name"],
    "url": f"{x['url']}/healthcheck",
} for x in instances]


# Write the config file
with open(".upptimerc.yml", "w", encoding="UTF-8") as f:
    yaml.safe_dump(config, f)
