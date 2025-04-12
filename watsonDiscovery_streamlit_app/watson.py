import os
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

load_dotenv()

authenticator = IAMAuthenticator(os.getenv("DISCOVERY_APIKEY"))
discovery = DiscoveryV2(
    version='2021-08-01',
    authenticator=authenticator
)
discovery.set_service_url(os.getenv("DISCOVERY_URL"))

def query_clause_similarity(clause_text):
    response = discovery.query(
        project_id=os.getenv("DISCOVERY_PROJECT_ID"),
        collection_ids=[os.getenv("DISCOVERY_COLLECTION_ID")],
        natural_language_query=clause_text,
        passages={
            "enabled": True,
            "count": 1
        }
    ).get_result()

    if 'passages' in response and response['passages']:
        passage = response['passages'][0]
        return {
            'match': passage['passage_text'],
            'score': passage['passage_score']
        }
    return { 'match': '', 'score': 0.0 }
