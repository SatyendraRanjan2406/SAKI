from django.test import TestCase
from .services.openAIService import generate_search_criteria

# Create your tests here.

class OpenAIServiceTest(TestCase):
    def test_generate_search_criteria(self):
        # Test with a sample query
        query = "Looking for a senior Python developer with 5+ years of experience in Django and React, based in Bangalore"
        result = generate_search_criteria(query)
        print("\nTest Query:", query)
        print("\nGenerated Criteria:", result)
