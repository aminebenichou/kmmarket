import json

# Load JSON data from file
with open('algeria_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract all commune_name values
commune_names = [item['commune_name_ascii'] for item in data]

# Remove duplicates using a set
unique_commune_names = list(set(commune_names))

# Optional: sort the list
unique_commune_names.sort()

# Write unique commune names to output JSON file
with open('unique_communes.json', 'w', encoding='utf-8') as f:
    json.dump(unique_commune_names, f, ensure_ascii=False, indent=2)

print(f"Saved {len(unique_commune_names)} unique commune names to unique_communes.json")