# from flask import Flask

# app = Flask(__name__)

import json
from google_api_v2 import adaptation_v2_inline_phrase_set,  adaptation_v2_inline_phrase_set_chirp, whisper_transcript
import os
from flask import Flask, request
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'google_secret_key.json'
app = Flask(__name__)


@app.route("/" , methods=["POST"])
def lambda_handler():
    if request.method == 'POST':
        event = request.json
        print('-----==-----' , request.method , event["transcriptType"])
        result = adaptation_v2_inline_phrase_set(event['audioUri'], event['transcriptType'])
        result1 = adaptation_v2_inline_phrase_set_chirp(event['audioUri'], event['transcriptType'])
        result2 = whisper_transcript(event['audioBase'], event['transcriptType'])
        
        print(result)
        print(result1)
        print(result2)
        
        return {
            'statusCode': 200,
            'body': result,
            'body1' : result1,
            'body2' : result2,
        }
    else:
            return {
                'statusCode': 400,
                'message':"Method Not Allowed"
            }

if __name__ == "__main__":
    app.run(debug=True)
    # ,host='0.0.0.0', port=8080