import json
import pytest
from dotenv import load_dotenv

from servicepad.models import User, Publication
from servicepad.app import create_app
from servicepad.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import UserFactory


register(UserFactory)

@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def another_user(db):
    user = User(
        username='another',
        email='another@mail.com',
        password='another'
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def publication_by_admin(db, admin_user):
    publication = Publication(
        title='title',
        description='description',
        user_id=admin_user.id
    )

    db.session.add(publication)
    db.session.commit()    

    return publication


@pytest.fixture
def publication_by_another(db, another_user):
    publication = Publication(
        title='title',
        description='description',
        user_id=another_user.id
    )

    db.session.add(publication)
    db.session.commit()    

    return publication


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }
