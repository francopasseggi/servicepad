import factory
from servicepad.models import User, Publication


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User


# class PublicationFactory(factory.Factory):

#     title = factory.Sequence(lambda n: "title%d" % n)
#     description = factory.Sequence(lambda n: "description%d" % n)
#     user_id = factory.Sequence(lambda n: n)

#     class Meta:
#         model = Publication
