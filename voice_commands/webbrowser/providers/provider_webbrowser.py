from stark.core.types import String
import urllib.parse


class WebBrowserProvider:

    def search(self, query: String) -> str:
        encoded_query = urllib.parse.quote(query.value)
        url = f"https://www.google.com/search?q={encoded_query}"
        return url
       #webbrowser.open(url)
        