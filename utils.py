import json

def convert_transcripts_to_json_objects(utterances):
    json_objects = []
    prev_role = None
    content_buffer = ""
    for utterance in utterances:
        role = 'assistant' if utterance['speaker'] == 0 else 'user'
        if role == prev_role:
            content_buffer += " " + utterance['transcript']
        else:
            if prev_role is not None:  
                json_objects.append({'role': prev_role, 'content': content_buffer})
            content_buffer = utterance['transcript']
            prev_role = role
    if content_buffer:
        json_objects.append({'role': prev_role, 'content': content_buffer})
    return json_objects


def convert_json_to_jsonl(conversation, filename='output.jsonl'):
    with open(filename, 'w') as file:
        for i in range(1, len(conversation), 2):
            if conversation[i-1]['role'] == 'assistant' and conversation[i]['role'] == 'user':
                prompt = conversation[i-1]['content']
                completion = conversation[i]['content']
                jsonl_object = {"prompt": prompt, "completion": completion}
                file.write(json.dumps(jsonl_object) + '\n')
    return filename