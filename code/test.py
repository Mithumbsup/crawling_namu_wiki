#소스 
#https://blessingdev.wordpress.com/2017/10/20/term-project-%EB%82%98%EB%AC%B4%EC%9C%84%ED%82%A4%EB%A5%BC-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95%EC%97%90-%EA%B4%80%ED%95%98%EC%97%AC/



import requests

def get_html(url):
    html =""
    resp = requests.get(url)

    if resp.status_code == 200:
        html = resp.text
    
    return html


# html = get_html('https://namu.wiki/w/%EA%B0%80%EC%A7%80(%EC%B1%84%EC%86%8C)')


target = "몬스테라"
# base_url = "https://namu.wiki/w/{}?from=URL".format(target)
base_url = "https://namu.wiki/w/{}".format(target)
html = get_html(base_url)
print(html)

