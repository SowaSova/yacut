from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validate_url


@app.route("/api/id/", methods=["POST"])
def add_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    short_id = data.get("custom_id") or get_unique_short_id()
    if not validate_url(short_id) or len(short_id) > 16:
        raise InvalidAPIUsage("Указано недопустимое имя для короткой ссылки")
    if URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')
    url_map = URLMap(original=data["url"], short=short_id)
    db.session.add(url_map)
    db.session.commit()
    return (
        jsonify(
            {
                "url": url_map.to_dict()["original"],
                "short_link": "http://localhost/"
                + url_map.to_dict()["short"],
            }
        ),
    )


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_id(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map:
        return jsonify(url=url_map.to_dict()["original"]), 200
    raise InvalidAPIUsage("Указанный id не найден", 404)
