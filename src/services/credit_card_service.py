from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.config import Config

def get_credit_card_info(image_url: str):
    try:
        credential = AzureKeyCredential(Config.SUBSCRIPTION_KEY)
        document_client = DocumentIntelligenceClient(Config.ENDPOINT, credential)

        result = document_client.begin_analyze_document("prebuilt-creditCard", AnalyzeDocumentRequest(url_source=image_url)).result()

        for doc in result.documents:
            fields = doc.fields

            return {
                "card_name": fields.get("CardHolderName", {}).get("content"),
                "card_number": fields.get("CardNumber", {}).get("content"),
                "bank_name": fields.get("IssuingBank", {}).get("content"),
                "expiration_date": fields.get("ExpirationDate", {}).get("content")
            }
    except Exception as e:
        print(e)
        return None
