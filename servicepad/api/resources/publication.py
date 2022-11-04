from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from servicepad.api.schemas import PublicationSchema
from servicepad.models import Publication
from servicepad.extensions import db
from servicepad.commons.pagination import paginate


class PublicationResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a publication
      description: Get a single publication by ID
      parameters:
        - in: path
          name: publication_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  publication: PublicationSchema
        404:
          description: publication does not exists
    put:
      tags:
        - api
      summary: Update a publication
      description: Update a single publication by ID
      parameters:
        - in: path
          name: publication_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              PublicationSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: publication updated
                  publication: PublicationSchema
        404:
          description: publication does not exists
    delete:
      tags:
        - api
      summary: Delete a publication
      description: Delete a single publication by ID
      parameters:
        - in: path
          name: publication_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: publication deleted
        404:
          description: publication does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, publication_id):
        user_id = get_jwt_identity()
        publication = Publication.query.filter_by(user_id=user_id, id=publication_id).first_or_404()

        schema = PublicationSchema()

        return {"publication": schema.dump(publication)}

    def put(self, publication_id):
        user_id = get_jwt_identity()
        publication = Publication.query.filter_by(user_id=user_id, id=publication_id).first_or_404()


        schema = PublicationSchema(partial=True)
        publication = schema.load(request.json, instance=publication)

        db.session.commit()

        return {"msg": "publication updated", "publication": schema.dump(publication)}

    def delete(self, publication_id):
        user_id = get_jwt_identity()
        publication = Publication.query.filter_by(user_id=user_id, id=publication_id).first_or_404()

        
        db.session.delete(publication)
        db.session.commit()

        return {"msg": "publication deleted"}, 204


class PublicationList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      summary: Get a list of publications
      description: Get a list of paginated publications
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/PublicationSchema'
    post:
      tags:
        - api
      summary: Create a publication
      description: Create a new publication
      requestBody:
        content:
          application/json:
            schema:
              PublicationSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: publication created
                  publication: PublicationSchema
    """

    method_decorators = [jwt_required()]

    def get(self):
        user_id = get_jwt_identity()

        schema = PublicationSchema(many=True)
        query = Publication.query.filter_by(user_id=user_id)
        return paginate(query, schema)

    def post(self):
        user_id = get_jwt_identity()

        schema = PublicationSchema()
        publication = schema.load(request.json)
        publication.user_id = user_id

        db.session.add(publication)
        db.session.commit()

        return {"msg": "publication created", "publication": schema.dump(publication)}, 201
