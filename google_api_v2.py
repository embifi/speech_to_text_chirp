
from google.cloud.speech_v2 import SpeechClient 
from google.cloud.speech_v2.types import cloud_speech
from flask import Flask, request, json
import re
from google.cloud import storage


import openai
import base64
import os
from google.api_core import client_options

openai.organization = "org-gfxrSGBOPq4XoXXv6L9vKY9h"
openai.api_key = "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"

def adaptation_v2_inline_phrase_set(
    # audio_file: str,
    audioUri: str,
    transcript_type: str,
) -> cloud_speech.BatchRecognizeResults:
    # cloud_speech.RecognizeResponse:
    # Instantiates a client
    client = SpeechClient()

  

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=["hi-IN", 'en-IN'],
        model="latest_long",
        # model="long",
    )
    
    audio = cloud_speech.BatchRecognizeFileMetadata(uri=audioUri)
    content = audio,
    print(audioUri);

    # Build inline phrase set to produce a more accurate transcript
    
    if transcript_type == "phone no":
        print("FULLPHONEUM CASE!!!!")
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$FULLPHONENUM", "boost": 20}])
    elif transcript_type == "address":
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$ADDRESSNUM", "boost": 20}])
    elif transcript_type == "bank name":
        phrase_set = cloud_speech.PhraseSet(phrases=[
          { "value": "HDFC", "boost": 20 },
          { "value": "ICICI", "boost": 20 },
          { "value": "Indusind", "boost": 20 },])
    elif transcript_type == "number":
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$OPERAND", "boost": 20}])
    elif transcript_type == "relation":
        phrase_set = cloud_speech.PhraseSet(phrases=[
          { "value": "Father", "boost": 20 },
          { "value": "Papa", "boost": 20 },
          { "value": "पिताजी", "boost": 20 },
          { "value": "अब्बा", "boost": 20 },
          { "value": "पिता", "boost": 20 },
          { "value": "बाप", "boost": 20 },])
    else:
        phrase_set = cloud_speech.PhraseSet(phrases=[])
    
    
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
            )
        ]
    )
    
  
    request = cloud_speech.BatchRecognizeRequest(
       recognizer=f"projects/77506381483/locations/global/recognizers/_",
        config=config,
        files=[audio],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )

    # Transcribes the audio into text
    
    operation = client.batch_recognize(request=request)
    # response = client.recognize(request=request)
    response = operation.result(timeout=120)
    
    output = response.results[audioUri]

    # print(output)
    
    if not output.transcript.results:
        resl = ""
        
    else:
        resl = output.transcript.results[0].alternatives[0].transcript
    
    print(f"Transcript: {resl}")
        
    cleaned_up_transcript = open_ai_cleanup(resl, transcript_type)
    print(cleaned_up_transcript)  
    
    return {"Transcript": resl, "cleanedUpTranscript": cleaned_up_transcript}

def adaptation_v2_inline_phrase_set_chirp(
    #  audio_file: str,
    audioUri: str,
    transcript_type: str,
) -> cloud_speech.BatchRecognizeResults:
# cloud_speech.RecognizeResponse:

    
    client_options_var = client_options.ClientOptions(
    api_endpoint="us-central1-speech.googleapis.com"
    )
    
    
    # Instantiates a client
    client = SpeechClient(client_options=client_options_var)
    audio = cloud_speech.BatchRecognizeFileMetadata(uri=audioUri)
    content = audio,
    print(audioUri);


    # Build inline phrase set to produce a more accurate transcript
    
    if transcript_type == "phone no":
        print("FULLPHONEUM CASE!!!!")
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$FULLPHONENUM", "boost": 20}])
    elif transcript_type == "address":
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$ADDRESSNUM", "boost": 20}])
    elif transcript_type == "bank name":
        phrase_set = cloud_speech.PhraseSet(phrases=[
          { "value": "HDFC", "boost": 20 },
          { "value": "ICICI", "boost": 20 },
          { "value": "Indusind", "boost": 20 },])
    elif transcript_type == "number":
        phrase_set = cloud_speech.PhraseSet(phrases=[{"value": "$OPERAND", "boost": 20}])
    elif transcript_type == "relation":
        phrase_set = cloud_speech.PhraseSet(phrases=[
          { "value": "Father", "boost": 20 },
          { "value": "Papa", "boost": 20 },
          { "value": "पिताजी", "boost": 20 },
          { "value": "अब्बा", "boost": 20 },
          { "value": "पिता", "boost": 20 },
          { "value": "बाप", "boost": 20 },])
    else:
        phrase_set = cloud_speech.PhraseSet(phrases=[])
    
    
    adaptation = cloud_speech.SpeechAdaptation(
        phrase_sets=[
            cloud_speech.SpeechAdaptation.AdaptationPhraseSet(
                inline_phrase_set=phrase_set
            )   
        ]
    )
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        # adaptation=adaptation,
        language_codes=["hi-IN"],
        model="chirp",
    )
    request = cloud_speech.BatchRecognizeRequest(
       recognizer=f"projects/77506381483/locations/us-central1/recognizers/_",
        config=config,
        files=[audio],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )
  

    # request = cloud_speech.RecognizeRequest(
    #     recognizer=f"projects/77506381483/locations/us-central1/recognizers/_",
    #     config=config,
    #     content=content,
    # )

    # Transcribes the audio into text
    # response = client.recognize(request=request)
    operation = client.batch_recognize(request=request)
    response = operation.result(timeout=120)
    output = response.results[audioUri]

    # print(output)
    
    if not output.transcript.results:
        resl = ""
        
    else:
        resl = output.transcript.results[0].alternatives[0].transcript
    
    print(f"Transcript: {resl}")
        
    cleaned_up_transcript = open_ai_cleanup(resl, transcript_type)
    print(cleaned_up_transcript)  
    
    return {"ChirpTranscript": resl, "cleanedUpTranscript": cleaned_up_transcript}


def open_ai_cleanup(transcribed_text, transcript_type):
    print(transcribed_text)
    
    
    
    if transcript_type == "phone no":
        print("openai called with phone no")
        gpt_prompt = "Reply only with a well formatted phone number, no other words. The phone number must be extracted from the given text (in case of no text given reply with 'no text input', if no phone number found in text reply with 'no phone number found'). Text: " + transcribed_text + "\n"
        print(gpt_prompt)
    elif transcript_type == "address":
        gpt_prompt = "Reply only with a well formatted address/place, no other words. The address/place must be extracted only from the given text (in case of no text given reply with 'no text input', if no address/place found in given text reply with 'no address found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "bank name":
        gpt_prompt = "Reply only with a well formatted bank name, no other words. The Bank name must be extracted from the given text (in case of no text given reply with 'no text input', if no Bank Name found in the given text reply with 'no bank name found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "number":
        gpt_prompt = "Reply only with a number, no other words. The number must be extracted from the given text (in case of no text given reply with 'no text input', if no number found in the given text reply with 'no number found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "relation":
        gpt_prompt = "Reply only with a single word, no other words. The word must be a relation (for example, father, mother, पिताजी, etc.) and must be extracted from the given text (in case of no text given reply with 'no text input', if no relation found in the given text reply with 'no relation found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "person name":
        gpt_prompt = "Reply only with a well formatted name of a person, no other words. The name must be extracted only from the given text (in case of no text given reply with 'no text input', if no name found in given text reply with 'no name found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "education":
        gpt_prompt = "Reply only with a well formatted level of of education (for example '10th', '12th', '8th', '10 वीं', '8 वीं', '12 वीं', etc.), no other words. The level of education must be extracted only from the given text (in case of no text given reply with 'no text input', if no education level found in given text reply with 'no education level found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "employment":
        gpt_prompt = "Reply only with a well formatted type/mode of employment, no other words. The type of employment must be extracted only from the given text (in case of no text given reply with 'no text input', if no employment type found in given text reply with 'no employment type found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "money":
        gpt_prompt = "Reply only with a well formatted money amount in rupees, no other words. The money amount must be extracted only from the given text (in case of no text given reply with 'no text input', if no money amount a found in given text reply with 'no monetary amount found'). Text: " + transcribed_text + "\n"
    elif transcript_type == "yesno":
        gpt_prompt = "Reply only with a well formatted 'yes' or 'no' or 'हाँ' or 'नहीं', no other words. The reply must be extracted only from the given text (in case of no text given reply with 'no text input', if no 'yes' or 'no' or 'हाँ' or 'नहीं' response is found in given text reply with 'no yes/no response found'). Text: " + transcribed_text + "\n"
    else:
        gpt_prompt = ""
    
    
    message=[{"role": "user", "content": gpt_prompt}]
    response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages = message,
    temperature=0.2,
    max_tokens=1000,
    frequency_penalty=0.0
    )
    print("openai response: ")
    print(response['choices'][0]['message']['content'])
    return response['choices'][0]['message']['content']
    
# # import tempfile

# # def whisper_transcript(base64Audio, transcript_type):
# #     try:
# #         # Create a temporary file to save the WAV data
# #         with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
# #             temp_wav.write(base64Audio)
# #             wav_file = temp_wav.name
       
# #     wav_file = open("/tmp/temp.wav", "wb")
# #     decode_string = base64.b64decode(base64Audio)
# #     wav_file.write(decode_string)
# #     audio_file= open("/tmp/temp.wav", "rb")
# #     transcript = openai.Audio.transcribe("whisper-1", audio_file)
# #     print("=======================")
# #     print("whisper transcript: " + transcript['text'])
# #     cleaned_up_res = open_ai_cleanup(transcript['text'], transcript_type)
# #     return {"whisperTranscript":transcript['text'], "cleanedupWhisperTranscript": cleaned_up_res}
  
# #      return "success"
# #     except Exception as e:
# #     return str(e)
import tempfile
import base64
import openai

def whisper_transcript(base64Audio, transcript_type):
    try:
        # Create a temporary file to save the WAV data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            decode_string = base64.b64decode(base64Audio)
            temp_wav.write(decode_string)
            wav_file_path = temp_wav.name

        with open(wav_file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            print("=======================")
            print("whisper transcript: " + transcript['text'])
            cleaned_up_res = open_ai_cleanup(transcript['text'], transcript_type)
            return {
                "whisperTranscript": transcript['text'],
                "cleanedupWhisperTranscript": cleaned_up_res
            }
        return "success"
    except Exception as e:
        return str(e)
