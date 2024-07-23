import requests
import json
import ast
import base64
from pathlib import Path

# Create a directory for the images if it doesn't exist
Path("./images").mkdir(parents=True, exist_ok=True)

def save_base64_image(base64_str, file_path):
    image_data = base64.b64decode(base64_str)
    with open(file_path, 'wb') as file:
        file.write(image_data)

url = "https://smartcitylivinglab.iiit.ac.in/ctop-api/nodes/get-node/WM12-0032-0001/latest"

response = requests.get(url)
data = response.json()
resp_text = data["m2m:cin"]["con"]
print(resp_text)


if isinstance(resp_text, str):
    try:
        resp_text = ast.literal_eval(resp_text)
    except ValueError:
        print("Error evaluating resp_text as a list.")
        exit()

if isinstance(resp_text, list) and len(resp_text) > 0:
    try:
        data = json.loads(resp_text[0])
    except json.JSONDecodeError:
        print("Error parsing the first element of resp_text as JSON.")
        exit()
else:
    print("resp_text is not a list or is empty.")
    exit()

# Extract Base64 values
bin1_base64 = data.get("Bin1", [None, None, None])[2]
bin2_base64 = data.get("Bin2", [None, None, None])[2]

# Print the values
print(f"BIN1: {bin1_base64}\n\nBIN2: {bin2_base64}")
save_base64_image(bin1_base64, './images/bin1_image.png')
save_base64_image(bin2_base64, './images/bin2_image.png')


print("Images saved successfully.")
