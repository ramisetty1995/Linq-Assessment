from app.extensions import session
def make_outbound_request(url):
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except session.Timeout:
        return {"message": "Request timed out."}
    except session.RequestException as e:
        return {"message": str(e)}

def normalize_note_fields(data):
    if 'note_body' in data:
        data['content'] = data.pop('note_body')
    if 'note_text' in data:
        data['content'] = data.pop('note_text')
    return data