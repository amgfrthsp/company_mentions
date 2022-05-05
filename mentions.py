import meduza_getter
import dostoevsky_classifier
import sqlite3
import json


def get_content(keywords):
    pubs = []
    pubs.extend(meduza_getter.getMeduzaMentionsByKeywords(keywords))
    # Vk, Google Play, ...
    return pubs


def classify_mentions(mentions):
    # TDO classify depending on type = news, post, comment etc
    return dostoevsky_classifier.classifyMentions(mentions)


def construct_query(keys):
    query = "INSERT INTO mentions ("
    params = "("
    for i in range(0, len(keys)):
        query += keys[i] + ("," if i < len(keys) - 1 else ")")
        params += "?" + ("," if i < len(keys) - 1 else ")")
    query += " VALUES " + params
    print(query)
    return query


def write_classified_mentions(classified_mentions, queryId):
    sqlite_connection = sqlite3.connect('/home/amgfrthsp/sqlite/db/test_mentions.db')
    cursor = sqlite_connection.cursor()

    keys = [
        "queryId",
        "url",
        "title",
        "timestamp",
        "content",
        "type",
        "verdict"]

    entries_dict = classified_mentions
    for entry in entries_dict:
        entry.update({"queryId": queryId})
        entry["verdict"] = json.dumps(entry["verdict"])

    entries = [tuple(entry[key] for key in keys) for entry in entries_dict]
    insert_query = construct_query(keys)
    cursor.executemany(insert_query, entries)
    sqlite_connection.commit()

    cursor.close()


def getMentionsByKeywords(keywords, queryId=0):
    mentions = get_content(keywords)

    classified_mentions = classify_mentions(mentions)

    write_classified_mentions(classified_mentions, queryId)
    return classified_mentions
