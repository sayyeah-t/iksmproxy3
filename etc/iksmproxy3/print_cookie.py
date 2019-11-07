from mitmproxy import http

trigger_url = "https://app.splatoon2.nintendo.net/?lang=ja-JP&na_country=JP&na_lang=ja-JP"

def request(flow: http.HTTPFlow):
    if flow.request.pretty_url == trigger_url:
        if "cookie" in flow.request.headers:
            print(flow.request.headers["cookie"])
