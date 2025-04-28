import json

def convert_string_to_json(byte_data):
    decoded_str = byte_data.decode('utf-8')

    # Convert the decoded string to JSON
    json_data = json.loads(decoded_str)
    return json_data