from flask import request

def parse_pagination(args):
    try:
        limit = int(args.get('limit', 20))
    except Exception:
        limit = 20
    try:
        offset = int(args.get('offset', 0))
    except Exception:
        offset = 0
    if limit > 100:
        limit = 100
    return limit, offset