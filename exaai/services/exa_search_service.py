from exa_py import Exa

class ExaService:
    def __init__(self, api_key):
        self.exa = Exa(api_key=api_key)

    def search_ai_blog_posts(self, query):
        try:
            result = self.exa.search_and_contents(query, text=True)
            return result
        except Exception as e:
            print(f"Error fetching from Exa API: {e}")
            return None
