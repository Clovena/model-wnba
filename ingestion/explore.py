import json
from extract.espn_client import get

# What does a single day's scoreboard look like?
data = get("scoreboard", params={"dates": "20250532"})

# Pretty print so we can see the full structure
print(json.dumps(data, indent=2))
