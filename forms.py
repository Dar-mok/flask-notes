"""Forms for playlist app."""

from wtforms import SelectField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Optional, Length


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField("Playlist Name", validators=[Length(min=1, max=50)])
    description = StringField("Describe it in less than 100 chars", validators=[Optional(), Length(min=1, max=100)])