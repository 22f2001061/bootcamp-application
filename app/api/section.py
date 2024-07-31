from flask_restful import Resource, Api, fields, marshal_with, reqparse, marshal

from app.models import Section
from app.db import db
from flask import Response

HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_500_SERVER_ERROR = 500


section_fields = {
    "section_id": fields.String,
    "section_name": fields.String,
}


section_parser = reqparse.RequestParser()
section_parser.add_argument("section_name")


class ListSectionResource(Resource):
    # listing of sections
    @marshal_with(section_fields)
    def get(self):
        sections = Section.query.all()
        return sections

    # create new section
    @marshal_with(section_fields)
    def post(self):
        args = section_parser.parse_args()
        print(args)
        section_name = args["section_name"]
        if section_name:
            new_section = Section(section_name=section_name)
            db.session.add(new_section)
            db.session.commit()
        else:
            return Response(
                {"message": "section_name is required"}, HTTP_400_BAD_REQUEST
            )
        return new_section

    def put(self):
        pass

    def delete(self):
        pass


class SectionResource(Resource):
    # Retrieve a single section with the given id
    @marshal_with(section_fields)
    def get(self, id):
        section = Section.query.get(id)
        return section

    # @marshal_with(section_fields)
    def put(self, id):
        args = section_parser.parse_args()
        updated_name = args["section_name"]
        if updated_name:
            existing_section = Section.query.get(id)
            if existing_section.section_name != updated_name:
                existing_section.section_name = updated_name
                db.session.add(existing_section)
                db.session.commit()
            return marshal(existing_section, section_fields), 201
        else:
            return Response(
                {"message": "section_name is required"}, HTTP_400_BAD_REQUEST
            )

    def delete(self, id):
        existing_section = Section.query.get(id)
        if existing_section:
            db.session.delete(existing_section)
            db.session.commit()
            return {"message": "Section Deleted Successfully!"}, 204
        else:
            return {"message": f"Section with {id} not found"}, HTTP_404_NOT_FOUND

    # create new section
    # @marshal_with(section_fields)
    # def post(self, id):
    #     pass
