import os
from flask import Flask, request
from werkzeug.exceptions import BadRequest


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route('/perform_query')
def post():
    try:
        query = request.args.get('query')
        file_name = request.args.get('file_name')
    except BadRequest as information_string:
        return information_string

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} не найден")

    with open(file_path) as f:
        result = analysis_query(f, query)
        data = '\n'.join(result)
        print(data)
    return app.response_class(data, content_type="text/plain")


def analysis_query(path, query):
    query_items = query.split("|")
    res = map(lambda v: v.strip(), path)
    for item in query_items:
        split_item = item.split(":")
        cmd = split_item[0]
        if cmd == "filter":
            arg = split_item[1]
            res = filter(lambda v, txt=arg: txt in v, res)
        if cmd == "map":
            arg = int(split_item[1])
            res = map(lambda v, idx=arg: v.split(" ")[idx], res)
        if cmd == "unique":
            res = set(res)
        if cmd == "sort":
            arg = split_item[1]
            reverse = arg == "desc"
            res = sorted(res, reverse=reverse)
        if cmd == "limit":
            arg = int(split_item[1])
            res = list(res)[:arg]
    return res
