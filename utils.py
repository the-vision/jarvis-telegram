import os

CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD'))
FALLBACK_INTENT = os.environ.get('FALLBACK_INTENT')


def extract_structured_data(result):
    data = {
        'intent': FALLBACK_INTENT,
        'entities': []
    }
    if result['intent']['confidence'] > CONFIDENCE_THRESHOLD:
        data['intent'] = result['intent']['name']
    for entity in result['entities']:
        if entity['confidence'] > CONFIDENCE_THRESHOLD:
            data['entities'].append({
                'name': entity['entity'],
                'value': entity['value']
            })
    return data


def log(conn, intent, entities, input, sender, postback):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO logs (intent, entities, input, sender, postback) VALUES (%s, %s, %s, %s, %s)", (intent, entities, input, sender, postback));
        conn.commit()
