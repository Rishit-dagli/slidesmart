import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction


def sample_extractive_summarization(document):
    endpoint = "https://hack121022.cognitiveservices.azure.com/"
    key = os.getenv("AZURE_API_KEY")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=20),
        ],
    )

    document_results = poller.result()
    for extract_summary_results in document_results:
        for result in extract_summary_results:
            if result.kind == "ExtractiveSummarization":
                print(
                    "Summary extracted: \n{}".format(
                        " ".join([sentence.text for sentence in result.sentences])
                    )
                )
            elif result.is_error is True:
                print(
                    "...Is an error with code '{}' and message '{}'".format(
                        result.code, result.message
                    )
                )

    result = text_analytics_client.extract_key_phrases(document)
    for idx, doc in enumerate(result):
        if not doc.is_error:
            print(
                "Key phrases in article #{}: {}".format(
                    idx + 1, ", ".join(doc.key_phrases)
                )
            )
