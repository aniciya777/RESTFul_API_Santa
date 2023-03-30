from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.groups import Group


def abort_if_not_found(cls, _id: int):
    session = db_session.create_session()
    data = session.query(cls).get(_id)
    if not data:
        abort(404, message=f"object <{cls.__name__}> with id {_id} not found")
        return None, session
    return data, session


group_parser = reqparse.RequestParser()
group_parser.add_argument('name', type=str, required=True)
group_parser.add_argument('description', type=str, required=False)

group_edit_parser = reqparse.RequestParser()
group_edit_parser.add_argument('name', type=str, required=False)
group_edit_parser.add_argument('description', required=False)


class GroupResource(Resource):
    def get(self, group_id: int):
        group, _ = abort_if_not_found(Group, group_id)
        return jsonify(group.to_dict(only=(
            'id', 'name', 'description', 'participants',
            'participants.id', 'participants.name', 'participants.wish',
            'participants.recipient.id',
            'participants.recipient.name',
            'participants.recipient.wish',
        )))
        #TODO Проверить, что нет лишних полей

    def put(self, group_id: int):
        group, session = abort_if_not_found(Group, group_id)
        args = group_edit_parser.parse_args()
        if 'name' in args and args['name']:
            group.name = args['name']
        if 'description' in args:
            group.description = args['description']
        session.merge(group)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, group_id: int):
        group, session = abort_if_not_found(Group, group_id)
        session.delete(group)
        session.commit()
        return jsonify({'success': 'OK'})


class NewGroupResource(Resource):
    def post(self):
        args = group_parser.parse_args()
        session = db_session.create_session()
        new_group = Group(
            name=args['name'],
            description=args['description'],
        )
        session.add(new_group)
        session.commit()
        return new_group.id


class GroupListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groups = session.query(Group).all()
        return jsonify([
            item.to_dict(only=('id', 'name', 'description'))
            for item in groups
        ])


