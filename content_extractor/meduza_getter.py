import meduza
import re


def get_meduza_pubs_for_companies(companies, maxSize=5):
    meduza_url_pub_map = {}
    for company_id_name in companies:
        company_id = company_id_name[0]
        company_name = company_id_name[1]
        pubs = meduza.search(company_name)
        for pub in pubs:
            if pub == {}:
                continue
            pub.update({"company_id": company_id})
            meduza_url_pub_map.update({pub["url"]: pub})
            if len(meduza_url_pub_map) >= maxSize:
                return list(meduza_url_pub_map.values())
    return list(meduza_url_pub_map.values())


def get_live_content(pub):
    content = ""
    body = pub["content"]
    if "lead" in body:
        for block in body["lead"]:
            if block["type"] == "rich_title":
                content += block["data"]["first"] + "\n"
                content += block["data"]["second"] + "\n"
            if block["type"] == "important_lead":
                for elem in block["data"]:
                    if elem["type"] == "ul":
                        for item in elem["data"]:
                            content += item + "\n"
    if ("broadcast" in body) and ("items" in body["broadcast"]):
        items = body["broadcast"]["items"]
        for item in list(items.values()):
            if "blocks" in item:
                content += parse_blocks(item["blocks"])
    return content


def parse_blocks(blocks):
    content = ""
    for block in blocks:
        if block["type"] == "p" or block["type"] == "h3" or block["type"] == "lead":
            content += block["data"]
        if block["type"] == "image":
            content += block["data"]["caption"] if "caption" in block["data"] else ""
        if block["type"] == "grouped":
            content += parse_blocks(block["data"])
        content += "\n"
    return content


def get_pub_content(pub):
    if pub["layout"] == "live":
        return get_live_content(pub)
    body = pub["content"]
    content = ""
    if "head" in body:
        for item in body["head"]:
            if item["type"] == "rich_title":
                content += item["data"]["first"] + "\n" if "first" in item["data"] else ""
                content += item["data"]["second"] + "\n" if "second" in item["data"] else ""
            if item["type"] == "simple_title":
                content += item["data"]["first"] + "\n"
    if "blocks" in body:
        content += parse_blocks(body["blocks"])
    if "slides" in body:
        for slide in body["slides"]:
            content += parse_blocks(slide["blocks"])
    return content


def get_meduza_mentions_for_companies(companies):
    pubs = get_meduza_pubs_for_companies(companies)
    mentions = []
    for pub in pubs:
        content = get_pub_content(pub)
        content = re.sub("<.*?>", "", content)
        mentions.append(dict({
            "url": "meduza.io/" + pub["url"],
            "company_id": pub["company_id"],
            "title": pub["title"],
            "timestamp": pub["datetime"],
            "content": content,
            "type": "news"
        }))
    return mentions

