from typing import List

def recompute_index(
    iterable: List,
    key: str
):
    return {
        getattr(item, key): i
        for i, item in enumerate(iterable)
    }