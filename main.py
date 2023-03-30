from flask import Flask, jsonify
from flask_restful import Api

from data import db_session
from group_resources import GroupListResource, NewGroupResource, GroupResource
from participant_resources import ParticipantResource, ParticipantListResource, RecipientResource


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yaprofi-restapi'
api = Api(app)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == '__main__':
    db_session.global_init("db/santa.db")
    api.add_resource(GroupListResource, '/groups')
    api.add_resource(NewGroupResource, '/group')
    api.add_resource(GroupResource, '/group/<int:group_id>')
    api.add_resource(ParticipantListResource, '/group/<int:group_id>/participant')
    api.add_resource(ParticipantResource, '/group/<int:group_id>/participant/<int:participant_id>')
    api.add_resource(RecipientResource, '/group/<int:group_id>/recipient/<int:participant_id>')

    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True
    )
