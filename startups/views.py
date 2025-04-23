import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class FetchStartupsView(APIView):
    def get(self, request):
        headers = {
            "Authorization": "Bearer SKX170L9yc-IcqeUNLVq01mGq1Gwrjlu6zYU_0szinU",  # Replace with your actual Product Hunt token
            "User-Agent": "Mozilla/5.0"
        }

        startups = []
        has_next_page = True
        end_cursor = None

        while has_next_page and len(startups) < 50:
            after_cursor = f', after: "{end_cursor}"' if end_cursor else ''
            query = f"""
            {{
              posts(order: VOTES, first: 20{after_cursor}) {{
                pageInfo {{
                  hasNextPage
                  endCursor
                }}
                edges {{
                  node {{
                    name
                    tagline
                    topics(first: 1) {{
                      edges {{
                        node {{
                          name
                        }}
                      }}
                    }}
                    votesCount
                    thumbnail {{
                      url
                    }}
                    url
                  }}
                }}
              }}
            }}
            """

            response = requests.post(
                'https://api.producthunt.com/v2/api/graphql',
                json={'query': query},
                headers=headers
            )

            # DEBUG OUTPUT
            print("📡 Status:", response.status_code)
            print("📡 Raw:", response.text[:500])

            if response.status_code != 200:
                return Response({
                    'error': 'Failed to fetch from Product Hunt',
                    'status_code': response.status_code,
                    'response_text': response.text[:500]
                }, status=response.status_code)

            try:
                response_json = response.json()

                if "errors" in response_json:
                    return Response({
                        "error": "GraphQL error",
                        "details": response_json["errors"]
                    }, status=500)

                posts_data = response_json.get("data", {}).get("posts", {})
                page_info = posts_data.get("pageInfo", {})
                edges = posts_data.get("edges", [])

                for edge in edges:
                    node = edge["node"]
                    startup = {
                        "name": node["name"],
                        "tagline": node["tagline"],
                        "category": node["topics"]["edges"][0]["node"]["name"] if node["topics"]["edges"] else "General",
                        "votes": node["votesCount"],
                        "logo_url": node["thumbnail"]["url"],
                        "product_url": node["url"]
                    }
                    startups.append(startup)

                has_next_page = page_info.get("hasNextPage", False)
                end_cursor = page_info.get("endCursor", None)

            except Exception as e:
                return Response({
                    "error": "Could not parse API response",
                    "details": str(e),
                    "raw": response.text[:500]
                }, status=500)

        print(f"✅ Total fetched: {len(startups)}")
        return Response(startups[:50])  # Only return up to 50 results
