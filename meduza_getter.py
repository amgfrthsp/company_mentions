import sys
import meduza
import dostoevsky


def getMeduzaPubsByKeywords(keywords, maxSize=20):
    meduzaUrlPubMap = {}
    for keyword in keywords:
        pubs = meduza.search(keyword)
        for pub in pubs:
            meduzaUrlPubMap.update({pub["url"]: pub})
            if len(meduzaUrlPubMap) >= maxSize:
                return list(meduzaUrlPubMap.values())
    return list(meduzaUrlPubMap.values())


def main() -> int:
    #keywords = input().split(' ')
    keywords = ['украина', 'крым', 'война']
    meduzaPubs = getMeduzaPubsByKeywords(keywords, 5)
    return 0


if __name__ == '__main__':
    sys.exit(main())
