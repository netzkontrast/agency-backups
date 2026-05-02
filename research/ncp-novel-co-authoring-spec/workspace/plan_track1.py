import json
import sys

def analyze_ncp_schema():
    with open('/tmp/ncp/schema/ncp-schema.json', 'r') as f:
        schema = json.load(f)

    print("Top Level Keys in definitions:")
    if "$defs" in schema:
        print(schema["$defs"].keys())

    print("\nProperties of story:")
    story_props = schema.get("properties", {}).get("story", {}).get("properties", {})
    print(story_props.keys())

    print("\nProperties of narratives:")
    narrative_props = story_props.get("narratives", {}).get("items", {}).get("properties", {})
    print(narrative_props.keys())

    subtext_props = narrative_props.get("subtext", {}).get("properties", {})
    print("\nSubtext properties:")
    print(subtext_props.keys())

    storytelling_props = narrative_props.get("storytelling", {}).get("properties", {})
    print("\nStorytelling properties:")
    print(storytelling_props.keys())

    ideation_props = story_props.get("ideation", {}).get("properties", {})
    print("\nIdeation properties:")
    print(ideation_props.keys())

if __name__ == "__main__":
    analyze_ncp_schema()
