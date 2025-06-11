import urllib.parse
import webbrowser


class WebBrowserProvider:

    def open_browser(self, query: str) -> str:
        webbrowser.open(self._get_google_url(query))

    def _get_google_url(self, query: str) -> str:
        encoded_query = urllib.parse.quote(query)
        return f"https://www.google.com/search?q={encoded_query}"
