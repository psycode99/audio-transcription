import requests
import config
import textwrap

API_KEY = config.api_key  # your  assembly ai api key
file_uploaded = 'Audio - Steve Jobs - Stay Hungry Stay Foolish.mp3'  # audio file to transcribe


def read_file(filename, chunk_size=5242880):
    """
    reads audio file
    :param filename: name of audio file to transcribe
    :param chunk_size:
    :return:
    """
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def transcribe():
    # api post request to get an audio url for the audio file uploaded
    headers = {'authorization': API_KEY}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(file_uploaded))
    result = response.json()

    # api post request to transcribe audio from audio url generated
    # from above api call
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": result['upload_url'],
        "auto_chapters": True,
        "entity_detection": True

    }
    headers = {
        "authorization": API_KEY,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    audio_result = response.json()

    # api get request to get the transcription result
    endpoint = f"https://api.assemblyai.com/v2/transcript/{audio_result['id']}"
    headers = {
        "authorization": API_KEY,
    }
    response = requests.get(endpoint, headers=headers)
    initial_result = response.json()

    # api get request to keep running until the status of the api response == 'completed'
    while initial_result['status'] != 'completed':
        endpoint = f"https://api.assemblyai.com/v2/transcript/{audio_result['id']}"
        headers = {
            "authorization": API_KEY,
        }
        response = requests.get(endpoint, headers=headers)
        final_result = response.json()
        if final_result['status'] == 'completed':
            print(final_result)
            print(response.status_code)

            # write the transcription result in a text file
            with open('transcription.txt', 'w') as file:
                output = final_result['text']
                file.write(textwrap.fill(output))
            break
        else:
            continue


transcribe()
