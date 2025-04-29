import re
from bs4 import BeautifulSoup

def result_to_dict(result):
    # Convert the Exa result into a dict (handle `Result` objects here)
    return {
        'results': [
            {
                'text': webset_result_to_dict(item),
             }
            for item in result
        ]
    }


def webset_result_to_dict(result):
    # Convert the Exa result into a dict (handle `Result` objects here)
    return {
        'results': [
            {
                'text': str(item),
             }
            for item in result
        ]
    }



def convert_to_readable_text(data):
    # Strip HTML tags using BeautifulSoup
    soup = BeautifulSoup(data, "html.parser")
    text = soup.get_text(separator="\n")

    # Remove markdown-style image syntax, links, and other special characters
    # Remove image URLs and markdown formatting (e.g., [text](url))
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove image links
    text = re.sub(r'\[([^\]]+)\]\((http[^\)]+)\)', r'\1: \2', text)  # Convert markdown links to plain text

    # Optional: Replace multiple newlines with a single newline for readability
    text = re.sub(r'\n+', '\n', text).strip()

    return text