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

def get_enrichment_payload(description, format_type="text", options=None, metadata=None):
    """
    Create payload for enrichment creation
    
    Args:
        description (str): Description of the enrichment
        format_type (str): Format type (default: "text")
        options (list): List of option dictionaries with "label" key
        metadata (dict): Additional metadata
    
    Returns:
        dict: Formatted payload
    """
    payload = {
        "description": description,
        "format": format_type,
        "options": options or [],
        "metadata": metadata or {}
    }
    return payload

def get_webhook_payload(events, url, metadata=None):
    """
    Create payload for webhook creation
    
    Args:
        events (list): List of events to subscribe to
        url (str): Webhook URL
        metadata (dict): Additional metadata
    
    Returns:
        dict: Formatted payload
    """
    payload = {
        "events": events,
        "url": url,
        "metadata": metadata or {}
    }
    return payload