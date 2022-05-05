import meduza
import re


def getMeduzaPubsByKeywords(keywords, maxSize=5):
    meduzaUrlPubMap = {}
    for keyword in keywords:
        pubs = meduza.search(keyword)
        for pub in pubs:
            if pub == {}:
                continue
            meduzaUrlPubMap.update({pub["url"]: pub})
            if len(meduzaUrlPubMap) >= maxSize:
                return list(meduzaUrlPubMap.values())
    return list(meduzaUrlPubMap.values())


def getLiveContent(pub):
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
                content += parseBlocks(item["blocks"])
    return content


def parseBlocks(blocks):
    content = ""
    for block in blocks:
        if block["type"] == "p" or block["type"] == "h3" or block["type"] == "lead":
            content += block["data"]
        if block["type"] == "image":
            content += block["data"]["caption"] if "caption" in block["data"] else ""
        if block["type"] == "grouped":
            content += parseBlocks(block["data"])
        content += "\n"
    return content


def getPubContent(pub):
    if pub["layout"] == "live":
        return getLiveContent(pub)
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
        content += parseBlocks(body["blocks"])
    if "slides" in body:
        for slide in body["slides"]:
            content += parseBlocks(slide["blocks"])
    return content


def getMeduzaMentionsByKeywords(keywords):
    pubs = getMeduzaPubsByKeywords(keywords)
    mentions = []
    for pub in pubs:
        content = getPubContent(pub)
        content = re.sub("<.*?>", "", content)
        mentions.append(dict({
            "url": "meduza.io/" + pub["url"],
            "title": pub["title"],
            "timestamp": pub["datetime"],
            "content": content,
            "type": "news"
        }))
    return mentions

