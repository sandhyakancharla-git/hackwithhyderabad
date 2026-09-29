import os, json
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()
_client = None

def get_client():
    global _client
    if _client is None:
        _client = Hindsight(
            base_url="https://api.hindsight.vectorize.io",
            api_key=os.getenv("HINDSIGHT_API_KEY")
        )
    return _client

def remember(service, fact):
    c = get_client()
    bank = f"service-{service}"
    try:
        c.banks.create(bank_id=bank, name=service)
    except:
        pass
    c.retain(bank_id=bank, content=fact)

def recall(service, query):
    c = get_client()
    bank = f"service-{service}"
    try:
        r = c.recall(bank_id=bank, query=query)
        return [x.text for x in r.results]
    except:
        return []

def seed_all():
    with open("data/incidents.json") as f:
        data = json.load(f)
    for service, info in data.items():
        c = get_client()
        bank = f"service-{service}"
        try:
            c.banks.create(bank_id=bank, name=service)
        except:
            pass
        c.retain(bank_id=bank, content=f"Service: {service}. Team: {info['team']}.")
        for inc in info.get("past_incidents", []):
            text = (f"On {inc['date']}, incident: {inc['symptom']}. "
                    f"Root cause: {inc['root_cause']}. "
                    f"Fix: {inc['fix']}. "
                    f"Resolved in {inc['resolved_in_minutes']} minutes.")
            c.retain(bank_id=bank, content=text)