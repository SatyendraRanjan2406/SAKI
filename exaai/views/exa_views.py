from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from SakiProject.settings import EXA_API_KEY
from exaai.services.exa_service import ExaService
from exaai.utils import result_to_dict
from webset.utils import convert_string_to_json

"""
    API :search the web and extract contents from the results.
    REQUEST_BODY :
    query= "Latest research in LLMs",
    type="auto/neural/keyword",
    category="company, research paper, news, pdf, github, tweet, personal site, linkedin profile, financial report ",
    num_results=10,
    text=True,
    include_domains=["arxiv.org", "paperswithcode.com"],
    exclude_domains=["arxiv.org", "paperswithcode.com"],
    start_crawl_data="2023-01-01T00:00:00.000Z",
    end_crawl_data="2023-12-31T00:00:00.000Z",
    startPublishedDate="2022-01-01T00:00:00.000Z",
    endPublishedDate="2022-12-31T00:00:00.000Z",
    includeText="2022-12-31T00:00:00.000Z",
    excludeText="2022-12-31T00:00:00.000Z",
    contents={
        text
        highlight
        summary
        livecrawl
        livecrawlTimeout
        subpages
        subpagesTarget
    },
    summary={
        "query": "Main developments"
    },
    subpages=1,
    subpage_target="sources",
    extras={
        "links": 1,
        "image_links": 1
    }
)
    

"""

class SearchAIBlogView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        exa_service = ExaService(api_key=EXA_API_KEY)

        query = convert_string_to_json(request.body).get('query')
        if query is None:
            return JsonResponse({'status': 'error', 'message': 'No query provided'},status=400)

        result = await exa_service.search_ai_blog_posts(query)

        if result and result.results:
            response_data = {
                "success": True,
                "message": "Search results fetched successfully.",
                "data": result_to_dict(result.results)
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                "success": False,
                "message": "No results found or API error.",
                "data": []
            }
            return JsonResponse(response_data, status=404)
