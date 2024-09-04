import requests, uuid, json
import pandas as pd

# Add your key, endpoint, and location (region)
key = " "  # Replace with your key
endpoint = "https://api.cognitive.microsofttranslator.com"  # Replace with your endpoint
location = "eastus"  # Replace with your location

# Construct the URL for the API
path = '/translate'
constructed_url = endpoint + path

# Parameters for the translation request
params = {
    'api-version': '3.0',
    'from': 'zh',  # From Chinese
    'to': ['vi']   # To Vietnamese (you can add more languages if needed)
}

# Headers with subscription details
headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Path to the input CSV file and output file
input_file = r" "
output_file = r" "

# Read the input CSV file
df = pd.read_csv(input_file, header=None)  # Change header according to your file if needed

# Create a function to translate text
def translate_text(text):
    body = [{'text': text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    
    # Print the response for debugging purposes
    print(f"Response for '{text}': {request.text}")

    # Check for errors in the response
    try:
        response = request.json()
        translated_text = response[0]['translations'][0]['text']
        return translated_text
    except (KeyError, IndexError) as e:
        print(f"Error occurred during translation: {e}")
        return text  # Return the original text if there's an error

# Translate each cell in the DataFrame
for col in df.columns:
    df[col] = df[col].apply(lambda x: translate_text(str(x)))  # Convert the text if it's not a string

# Save the translated DataFrame to a new CSV file
df.to_csv(output_file, index=False, header=False, encoding='utf-8')

print(f"Translation completed. Translated file saved to {output_file}")
