import requests 
 
# Define the base URL of your API 
base_url = 'http://127.0.0.1:8000/Get_Inference' 
# Set up the query parameters 
WavPath = r"path\to\your\speaker.wav"
params = { 
    'text': 'હેલો, કેમ છો? બધા સારા છો?', 
    'lang': 'gujarati',
} 
# Send the GET request 
with open(WavPath, "rb") as AudioFile: 
    response = requests.post(base_url, params = params,  files = { 'speaker_wav': AudioFile.read() }) 
 
# Check if the request was successful 
if response.status_code == 200: 
    # Save the audio content to a file
    with open('output.wav', 'wb') as f:
        f.write(response.content)
    print("Audio saved as 'output.wav'")
else:
# Print the error message
    print(f"Request failed with status code {response.status_code}")
    print("Response:", response.text)