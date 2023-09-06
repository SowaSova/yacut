from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(min=1),
            URL(),
        ],
    )
    custom_id = URLField(
        "Ваш вариант короткой ссылки",
        validators=[
            Optional(),
            Regexp(
                r"^[a-zA-Z0-9_]+$",
                message="Указано недопустимое имя для короткой ссылки",
            ),
            Length(1, 16),
        ],
    )
    submit = SubmitField("Создать")
