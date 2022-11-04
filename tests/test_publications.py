from flask import url_for

from servicepad.models import Publication


def test_get_publication(client, db, publication_by_admin, publication_by_another, admin_headers):
    # test 404
    publication_url = url_for('api.publication_by_id', publication_id="100000")
    rep = client.get(publication_url, headers=admin_headers)
    assert rep.status_code == 404

    # test get_publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_admin.id)
    rep = client.get(publication_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["publication"]
    assert data["title"] == publication_by_admin.title
    assert data["description"] == publication_by_admin.description

    # test get another user's publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_another.id)
    rep = client.get(publication_url, headers=admin_headers)
    assert rep.status_code == 404



def test_put_publication(client, db, publication_by_admin, publication_by_another, admin_headers):
    # test 404
    publication_url = url_for('api.publication_by_id', publication_id="100000")
    rep = client.put(publication_url, headers=admin_headers)
    assert rep.status_code == 404

    data = {"title": "updated", "description": "new description"}

    # test update own publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_admin.id)
    rep = client.put(publication_url, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["publication"]
    assert data["title"] == "updated"
    assert data["description"] == "new description"

    # test update other user's publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_another.id)
    rep = client.put(publication_url, json=data, headers=admin_headers)
    assert rep.status_code == 404


def test_delete_publication(client, db, publication_by_admin, publication_by_another, admin_headers):
    # test 404
    publication_url = url_for('api.publication_by_id', publication_id="100000")
    rep = client.delete(publication_url, headers=admin_headers)
    assert rep.status_code == 404


    # test delete own publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_admin.id)
    rep = client.delete(publication_url, headers=admin_headers)
    assert rep.status_code == 204

    # test delete other user's publication
    publication_url = url_for('api.publication_by_id', publication_id=publication_by_another.id)
    rep = client.delete(publication_url, headers=admin_headers)
    assert rep.status_code == 404


def test_create_publication(client, db, admin_headers):
    data = {"title": "new publication", "description": "new description"}

    # test create publication
    publication_url = url_for('api.publications')
    rep = client.post(publication_url, json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()["publication"]
    assert data["title"] == "new publication"
    assert data["description"] == "new description"

    publication = Publication.query.get(data["id"])
    assert publication is not None
    assert publication.title == "new publication"
    assert publication.description == "new description"


def test_get_all_publications(client, db, publication_by_admin, publication_by_another, admin_headers):
    # test get all publications
    publication_url = url_for('api.publications')
    rep = client.get(publication_url, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["results"]
    assert len(data) == 1

    publication = data[0]
    assert publication["title"] == publication_by_admin.title
    assert publication["description"] == publication_by_admin.description

