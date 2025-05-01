import json

import os
from dotenv import load_dotenv

load_dotenv()

def convert_string_to_json(byte_data):
    decoded_str = byte_data.decode('utf-8')

    # Convert the decoded string to JSON
    json_data = json.loads(decoded_str)
    return json_data


def string_to_json(json_string):
    """
    Convert a JSON string to a Python dictionary.

    Args:
        json_string (str): The JSON string to convert

    Returns:
        dict: The parsed JSON object
    """
    try:
        # Remove any leading/trailing whitespace and newlines
        json_string = json_string.strip()
        # Parse the JSON string
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError as e:
        return {"success": False, "message": f"Error parsing JSON: {str(e)}"}


def get_exa_api_headers():
    """
    Get the headers for Exa.ai API requests
    """
    return {
        "x-api-key": os.getenv('EXA_API_KEY'),
        "Content-Type": "application/json"
    }


def get_exa_api_headers():
    """
    Get the headers for Exa.ai API requests
    """
    return {
        "x-api-key": os.getenv('EXA_API_KEY'),
        "Content-Type": "application/json"
    }

def get_webset_update_payload(metadata=None):
    """
    Get the payload for updating webset metadata
    Args:
        metadata (dict, optional): Metadata to update. Defaults to empty dict.
    Returns:
        dict: Payload for the update request
    """
    return {
        "metadata": metadata or {}
    } 