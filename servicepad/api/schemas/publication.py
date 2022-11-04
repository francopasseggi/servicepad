from servicepad.models import Publication
from servicepad.extensions import ma, db
import datetime as dt



class PublicationSchema(ma.SQLAlchemyAutoSchema):
    time_since_publication = ma.Method("get_time_since_publication", dump_only=True)

    def get_time_since_publication(self, obj):
        return str(dt.datetime.now() - obj.created_at)


    class Meta:
        model = Publication
        sqla_session = db.session
        load_instance = True
        exclude = ("user_id",)
        dump_only = ("id", "created_at", "updated_at")
