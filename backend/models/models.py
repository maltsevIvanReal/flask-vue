from flask_login import UserMixin

from config import *

UserRoles = db.Table('UserRoles',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

users_to_groups_table = db.Table('users_to_groups_table',
                                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                 db.Column('group_id', db.Integer, db.ForeignKey('group.id')))

groups_to_roles_table = db.Table('groups_to_roles_table',
                                 db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
                                 db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                                 )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    _roles = db.relationship("Role", secondary=UserRoles)
    _groups = db.relationship("Group", secondary=users_to_groups_table)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            '_roles': [i.serialize for i in self._roles],
            '_groups': [i.serialize for i in self._groups]
        }


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users = db.relationship("User", backref="groups", secondary=users_to_groups_table)
    _roles = db.relationship("Role", secondary=groups_to_roles_table)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            '_roles': [i.serialize for i in self._roles],
            'users': [{'name': i.name, 'id': i.id} for i in self.users]

        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship("User", backref="roles", secondary=UserRoles)
    groups = db.relationship("Group", backref="roles", secondary=groups_to_roles_table)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'users': [{'name': i.name, 'id': i.id} for i in self.users],
            'groups': [{'name': i.name, 'id': i.id} for i in self.groups]

        }
