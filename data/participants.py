import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Participant(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'participants'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    wish = sa.Column(sa.String, nullable=True)
    recipient_id = sa.Column(sa.Integer, sa.ForeignKey('participants.id'), nullable=True)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('groups.id'), nullable=False)

    recipient = orm.relationship('Participant', uselist=False)
    group = orm.relationship('Group')
