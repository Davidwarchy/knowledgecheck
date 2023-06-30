import requests
import xml.etree.ElementTree as ET
from functools import lru_cache

DBPEDIA_API = "http://lookup.dbpedia.org/api/search/KeywordSearch"

def parse_dbpedia_result(result):
    return {
        "label": result.find("Label").text,
        "uri": result.find("URI").text,
        "description": result.find("Description").text,
        "classes": [
            {"label": cls.find("Label").text, "uri": cls.find("URI").text}
            for cls in result.find("Classes")
        ],
        "categories": [
            {"uri": cat.find("URI").text}
            for cat in result.find("Categories")
        ],
    }

def satisfy_query_dbpedia(query, result):
    return query.lower() in result["label"].lower()

def get_categories_dbpedia(result):
    return [cls["uri"].split('/')[-1] for cls in result["classes"]]

@lru_cache(maxsize=100)  # You can adjust the 'maxsize' parameter based on your needs
def search_dbpedia(query, limit=10):
    response = requests.get(
        DBPEDIA_API,
        headers={"Accept": "application/xml"},
        params={"QueryString": query, "MaxHits": limit},
    )
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        results = [parse_dbpedia_result(result) for result in root.findall("Result")]
        return results
    else:
        return []

def find( query ):
    results = search_dbpedia(query)
    response = []
    for result in results:
        if satisfy_query_dbpedia(query, result):
            res =   { 
                     'label': result['label'],
                     'uri': result['uri'],
                     'categories': get_categories_dbpedia(result)
                    }
            response.append( res )
            print(f"Matched: {result['label']} ({result['uri']})")
            print(f"Categories: {get_categories_dbpedia(result)}")
    
    if response != []:
        return response 

if __name__ == "__main__":
    find("Antoine")
