from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.groups import Group
from data.participants import Participant


participant_parser = reqparse.RequestParser()
participant_parser.add_argument('name', type=str, required=True)
participant_parser.add_argument('wish', type=str, required=False)


def abort_if_not_found(cls, _id: int, session=None):
    if session is None:
        session = db_session.create_session()
    data = session.query(cls).get(_id)
    if not data:
        abort(404, message=f"object <{cls.__name__}> with id {_id} not found")
        return None, session
    return data, session


class RecipientResource(Resource):
    def get(self, group_id: int, participant_id: int):
        session = db_session.create_session()
        group, _ = abort_if_not_found(Group, group_id, session)
        participant, _ = abort_if_not_found(Participant, participant_id, session)
        if participant not in group.participants:
            abort(404, message=f"object <Participant> with id {participant_id} not found")
        if participant.recipient is None:
            abort(404, message=f"recipient for object <Participant> with id {participant_id} not found")
        return jsonify(participant.recipient.to_dict(only=(
            'id', 'name', 'wish'
        )))


class ParticipantResource(Resource):
    def delete(self, group_id: int, participant_id: int):
        session = db_session.create_session()
        group, _ = abort_if_not_found(Group, group_id, session)
        participant, _ = abort_if_not_found(Participant, participant_id, session)
        if participant not in group.participants:
            abort(404, message=f"object <Participant> with id {participant_id} not found")
        group.participants.remove(participant)
        session.delete(participant)
        session.commit()
        return jsonify({'success': 'OK'})


class ParticipantListResource(Resource):
    def post(self, group_id: int):
        group, session = abort_if_not_found(Group, group_id)
        args = participant_parser.parse_args()
        new_participant = Participant(
            name=args['name'],
            wish=args['wish'],
        )
        group.participants.append(new_participant)
        session.merge(new_participant)
        session.commit()
        return new_participant.id
