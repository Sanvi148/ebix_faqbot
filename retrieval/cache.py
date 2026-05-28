import json
import os

CACHE_FILE = "cache/query_cache.json"

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cache,
            f,
            indent=4,
            ensure_ascii=False
        )


def get_cached_answer(query):
    cache = load_cache()
    return cache.get(query.lower())


def store_answer(query, answer):
    cache = load_cache()
    cache[query.lower()] = answer
    save_cache(cache)