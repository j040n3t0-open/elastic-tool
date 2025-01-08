import random, json, re

json_file_path = "/home/joaoneto/projetos/scripts/elastic-tool/template.json"

# Open the JSON file for reading
with open(json_file_path, "r") as json_file:
    data = json_file.read()

data = data.split('"""')
new_data = []
for part in data:
    if not "{" in part:
        part = part.replace('"',"'")
        new_data.append(part)
    else:
        new_data.append(part)

data = "\"".join(new_data)
data = json.loads(data)
print(data['took'])