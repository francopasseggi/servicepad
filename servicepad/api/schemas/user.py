from servicepad.models import User
from servicepad.extensions import ma, db
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)
    photo = fields.Raw(metadata={'type': 'string', 'format': 'binary'}, required=False)

    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)

