from django.shortcuts import render

from SakiProject.settings import EXA_API_KEY
from exaai.services.exa_search_service import ExaService

# Ideally, move API keys to environment variables or settings

def search_ai_blog(request):
    context = {}
    if request.method == 'GET':
        exa_service = ExaService(api_key=EXA_API_KEY)
        query = "blog post about AI"
        result = exa_service.search_ai_blog_posts(query)

        context['results'] = result.results if result else []

    return render(request, 'search_results.html', context)
