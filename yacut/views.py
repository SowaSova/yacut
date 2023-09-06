from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def index_view():
    template = "index.html"
    form = URLForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data or get_unique_short_id()
        url_map = URLMap.query.filter_by(short=short_url).first()
        if url_map:
            flash(f"Имя {short_url} уже занято!", "error-message")
        else:
            url_map = URLMap(
                original=form.original_link.data, short=short_url
            )
            db.session.add(url_map)
            db.session.commit()
            flash("Ваша новая ссылка готова:", "success-message")
            flash(f"{short_url}", "result")
            return (
                render_template(template, form=form, custom_id=short_url),
                200,
            )
    return render_template(template, form=form)


@app.route("/<string:custom_id>", methods=["GET"])
def redirect_view(custom_id):
    url_map = URLMap.query.filter_by(short=custom_id).first()
    if url_map:
        return redirect(url_map.original, 302)
    else:
        abort(404)
