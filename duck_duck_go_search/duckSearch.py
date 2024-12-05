from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel
from typing import List

search = DuckDuckGoSearchResults(backend="news",output_format="list")

class DuckDuckGoSearchResults(BaseModel):
    snippet: str
    title: str
    link: str
    date: str
    source: str

def search_news_duckduckgo(query)-> List[DuckDuckGoSearchResults]:
    """
    :param query:
    :return: list of news articles from DuckDuckGo search
    """
    try:
        return [DuckDuckGoSearchResults(**news) for news in search.invoke(query)]
    except Exception as e:
        print(f"Error searching news: {e}")
        return []

print(search_news_duckduckgo("OpenAI"))