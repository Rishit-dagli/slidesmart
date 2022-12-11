from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
import requests
import time
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import (
    TextAnalyticsClient,
    ExtractSummaryAction
)
import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
import keras_cv
import requests
import urllib.request
from PIL import Image
from io import BytesIO
import marshal
import types


def index(request):
    context = {}

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        context.update({'uploaded_file_url': uploaded_file_url})

    return render(request, 'index.html', context=context)


@require_POST
def receive_audio(request):
    try:
        chapters, auto_highlights_result = audio_summarization(request.POST.get("audio_link"))
    except:
        pass

    return redirect('index')


@require_POST
def receive_text(request):
    try:
        myfile = request.FILES['myfile']
        with open(myfile.name, 'r') as f:
            summary, keywords = sample_extractive_summarization([f.read().rstrip()])
            print(summary)
            print(keywords)
    except:
        pass

    return redirect('index')


def sample_extractive_summarization(document):
    """Get summarization and keywords of .txt file"""
    endpoint = "https://hack121022.cognitiveservices.azure.com/"
    key = settings.AZURE_API_KEY

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count = min(20, int(len(document[0])*0.1))),
        ],
    )

    summary, keywords = '', ''

    document_results = poller.result()
    for extract_summary_results in document_results:
        for result in extract_summary_results:
            # if result.kind == "ExtractiveSummarization":
                print("Summary extracted: \n{}".format(
                    " ".join([sentence.text for sentence in result.sentences]))
                )
                summary = " ".join([sentence.text for sentence in result.sentences])
            # elif result.is_error is True:
            #     print("...Is an error with code '{}' and message '{}'".format(
            #         result.code, result.message
            #     ))
    
    result = text_analytics_client.extract_key_phrases(document)
    for idx, doc in enumerate(result):
        if not doc.is_error:
            print("Key phrases in article #{}: {}".format(
                idx + 1,
                ", ".join(doc.key_phrases)
            ))
            keywords = ", ".join(doc.key_phrases)
    
    return summary, keywords


def audio_summarization(audio_link):
    """Get summarization of audio using AssemblyAI API"""
    import pprint
    import requests
    import time

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": audio_link,
        "auto_highlights": True,
        "auto_chapters": True
    }
    headers = {
        "authorization": settings.ASSEMBLYAI_API_KEY,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    pprint.pprint(response.json())

    endpoint = "https://api.assemblyai.com/v2/transcript/" + response.json()["id"]
    headers = {
        "authorization": settings.ASSEMBLYAI_API_KEY,
    }
    response = requests.get(endpoint, headers=headers)

    while response.json()["auto_highlights_result"] == None:
        time.sleep(2)
        response = requests.get(endpoint, headers=headers)

    pprint.pprint(response.json()["chapters"])
    pprint.pprint(response.json()["auto_highlights_result"])
    pprint.pprint(response.json()["status"])

    return response.json()["chapters"], response.json()["auto_highlights_result"]


def generate_images():
    with open('serialized_bin', 'rb') as f:
        serialized = marshal.loads(f.read())
        predict = types.FunctionType(serialized, globals(), "predict")