import os
import time
import datetime
import wiotp.sdk.device
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import playsound

authenticator = IAMAuthenticator('yXCidqZMRPj4qvA3MAhiY7DznWLsO_cEf3urYEt1BFpP')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
    )

text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/77cfc001-dd6d-49eb-bd6a-92e3a040f2d4')

myConfig = { 
    "identity": {
        "orgId": "ujiha4",
        "typeId": "Esp32",
        "deviceId": "12345"
    },
    "auth": {
        "token": "12345678"
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

def myCommandCallback(cmd):
    print("Message recieved from IBM Iot Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    with open('medicine.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'You have to take '+m+' medicine Right now',
                voice='en-US_AllisonV3Voice',
                accept = 'audio/mp3'
            ).get_result().content)
    playsound.playsound('medicine.mp3')
    os.remove('medicine.mp3')
while True:    
    client.commandCallback = myCommandCallback
client.disconnect()
