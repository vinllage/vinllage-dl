import requests
from bs4 import BeautifulSoup as bs

def get_data(url, selector, url_prefix, keywords = []):
    
    response = requests.get(url)
    html_text = response.text

    soup = bs(html_text, 'html.parser')
    
    link_selector, title_selector, date_selector, content_selector = selector

    link_tags = soup.select(link_selector)
    items = []
    for tag in link_tags:

        link = tag.attrs['href']
        if not link: continue

        link = f'{url_prefix}{link}'

        res = requests.get(link)
        _soup = bs(res.text, "html.parser")

        # 게시글 제목 
        el = _soup.select_one(title_selector)
        title = el.get_text().strip() if el else None
        result = all(list(map(lambda x: x in title, keywords)))
        if not result: continue

        # 등록일
        el = _soup.select_one(date_selector)
        date = el.get_text().replace("작성일", "").replace("등록일", "").replace(".", "-").strip() if el else None
    
        # 게시글 내용 
        is_html = False
        els = _soup.select(f"{content_selector} p")
        if els:
            content = "\n".join([el.get_text() for el in els])
        else:
            el = _soup.select_one(f"{content_selector}")
            content = el.decode_contents().strip() if el else None
            if content: is_html = True

        # 게시글에 포함된 이미지 주소
        els = _soup.select(f"{content_selector} p img")
        images = [el.attrs['src'] for el in els if el]

        items.append({"date": date, "link": link, "title": title, "content": content, "image":images, "is_html": is_html})

    return items