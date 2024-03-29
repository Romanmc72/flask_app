#!/usr/bin/env python3
"""
This file contains database models for the application
"""
import os
from time import time

import jwt
from jwt.exceptions import DecodeError
from jwt.exceptions import InvalidTokenError
from jwt.exceptions import InvalidSignatureError
from jwt.exceptions import ExpiredSignatureError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import app
from app import db
from app import login

DEFAULT_SCHEMA = {"schema": os.getenv('DEFAULT_SCHEMA', 'flask_app')}
TOKEN_EXPIRE = 600
ALGORITHM = 'HS256'


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, str) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Score(CRUDMixin, db.Model):
    """
    Description
    -----------
    This saves the score for a particular game run and will likewise retrieve
    the highest score if that ever changes.
    """
    __table_args__ = DEFAULT_SCHEMA
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    score = db.Column(db.Integer, index=True)
    token_used = db.Column(db.Boolean)
    created_at = db.Column(db.Numeric(precision=16, scale=6))
    last_modified_at = db.Column(db.Numeric(precision=16, scale=6))

    def __repr__(self):
        """Returns a string representation of the score"""
        return f"<Score: {self.score}>"

    def get_high_score(self):
        """Returns the highest score from the Score table or 0 if there are no scores yet"""
        query = db.session.query(db.func.max(Score.score))
        result = db.session.execute(query).scalar()
        if result:
            return result
        else:
            return 0

    def issue_web_token(self, expires_in: int = 60 * 60):
        """
        Issues a json web token for the user to authenticate requests.
        There is really no way to prevent someone from hacking the high score
        list but this is an attempt to obfuscate some of the API details.

        By default the tokens will expire in 1 hour. Feel free to override
        that with the number of seconds that feels right to you.
        """
        return jwt.encode(
            {'id': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm=ALGORITHM
        ).decode('utf-8')

    @staticmethod
    def verify_web_token(token):
        """Decodes the json web tokens that were issued for submitting score changes."""
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=[ALGORITHM]
            )['id']
        except DecodeError or InvalidTokenError or InvalidSignatureError or ExpiredSignatureError:
            return None
        return Score.get_by_id(id)

    @staticmethod
    def get_user_best_scores(username: str, best_n: int = 10) -> list:
        """Get the top 10 scores for a given user"""
        sql_stmt = db.text("""
            SELECT
                score
                , last_modified_at AS date
            FROM
                flask_app.score
            WHERE
                username = :username
                AND token_used
            ORDER BY
                score DESC
                , last_modified_at DESC
            LIMIT :n;""")
        results = db.engine.execute(sql_stmt, {'username': username, 'n': best_n})
        return [{'score': record[0], 'date': record[1]} for record in results]

    @staticmethod
    def get_user_stats(username: str) -> dict:
        """Get some stats on the average performance of a given username"""
        sql_stmt = db.text("""
            SELECT
                AVG(score) AS avg_score
                , SUM(last_modified_at - created_at) AS seconds_played
                , COUNT(*) AS games_played
            FROM
                flask_app.score
            WHERE
                username = :username
                AND token_used""")
        results = db.engine.execute(sql_stmt, {'username': username}).first()
        if results[2] > 0:
            return {'average_score': float(results[0]), 'seconds_played': float(results[1]), 'games_played': results[2]}
        else:
            return {'average_score': 0, 'seconds_played': 0, 'games_played': 0}

    @staticmethod
    def get_best_scores(best_n: int = 10) -> list:
        """Get the top 10 scores for a given user"""
        sql_stmt = db.text("""
            SELECT
                username
                , score
                , last_modified_at AS date
            FROM
                flask_app.score
            WHERE
                token_used
            ORDER BY
                score DESC
                , last_modified_at DESC
            LIMIT :n;""")
        results = db.engine.execute(sql_stmt, {'n': best_n})
        return [{'username': record[0] or 'anon', 'score': record[1], 'date': record[2]} for record in results]


class User(UserMixin, db.Model):
    """
    Description
    -----------
    This class defines the User
    object to represent a particular
    user for the application and will be
    stored in the database associated
    with the flask application
    """
    __table_args__ = DEFAULT_SCHEMA
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.Numeric(precision=16, scale=6), nullable=False)
    last_modified_at = db.Column(db.Numeric(precision=16, scale=6), nullable=False)
    temp_start = db.Column(db.Numeric(precision=16, scale=6), nullable=True)
    temp_end = db.Column(db.Numeric(precision=16, scale=6), nullable=True)

    def __repr__(self) -> str:
        """Returns a string representation of the User"""
        return f"User <{self.username}>"

    def __todict__(self) -> dict:
        """Returns a dictionary representation of the user"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': float(self.created_at),
            'last_modified_at': float(self.last_modified_at),
            'temp_start': float(self.temp_start) if self.temp_start is not None else self.temp_start,
            'temp_end': float(self.temp_end) if self.temp_end is not None else self.temp_end
        }

    @staticmethod
    def from_dict(d: dict):
        """
        Create a user object based on a python dict.
        The dict keys must map to the User attributes exactly.
        """
        now = time()
        d['created_at'] = now
        d['last_modified_at'] = now
        try:
            password = d.pop('password')
            user = User(**d)
            user.set_password(password)
        except KeyError:
            if d.get('password_hash'):
                user = User(**d)
            else:
                raise KeyError('Required attributes include `password` or `password_hash`.')
        return user

    def update_from_dict(self, d: dict):
        """pass in a dict and update the user's attributes."""
        for k, v in d.items():
            self.__setattr__(k, v)
        return self

    def set_password(self, password: str) -> None:
        """
        Description
        -----------
        This function sets a password hash based on the password input

        Params
        ------
        :password: str
        A password to be hashed, this hashed password will be assigned
        to self.password_hash for the current user

        Return
        ------
        None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Description
        -----------
        This function checks a password against the password hash stored in the database

        Params
        ------
        :password: str
        The password checked against the particular user

        Return
        ------
        bool
        Whether or not the provided password matches the password hash
        """
        return check_password_hash(self.password_hash, password)

    def get_password_reset_token(self, expires_in: int = TOKEN_EXPIRE) -> str:
        """
        Description
        -----------
        This function takes the user's ID, the application's secret key and the token expiration
        time and returns a string representation of the token which can be used externally to
        validate a user's identity and reset their password.

        Params
        ------
        :expires_in: int
        The number of seconds that the json web token will be active for before it expires.

        Return
        ------
        str
        The string representation of the json web token.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm=ALGORITHM
        ).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token: str):
        """
        Description
        -----------
        This function takes in a json web token and either
        outputs the associated user or returns None.

        Params
        ------
        :token: str
        The json web token in string form.

        Return
        ------
        The user associated to the user id.
        """
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=[ALGORITHM]
            )['reset_password']
        except DecodeError or InvalidTokenError or InvalidSignatureError or ExpiredSignatureError:
            return None
        return User.query.get(id)

    def get_admin_token(self, expires_in: int = TOKEN_EXPIRE) -> str:
        """If this user is an admin, then they can get a token for admin APIs."""
        if self.role == 'admin':
            return jwt.encode(
                {'admin_id': self.id, 'exp': time() + expires_in},
                app.config['SECRET_KEY'],
                algorithm=ALGORITHM
            ).decode('utf-8')

    @staticmethod
    def verify_admin_token(token: str):
        """
        Verifies whether or not an admin token is valid.
        Returns the user if it is valid or None if it is not.
        """
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=[ALGORITHM]
            )['admin_id']
        except DecodeError or InvalidTokenError or InvalidSignatureError or ExpiredSignatureError:
            return None
        return User.query.get(id)

    @staticmethod
    def get_users(limit: int = 10, page: int = 1) -> list:
        """Find all users in the db and return them as a dict with pagination"""
        return [
            {
                "username": each_user.username,
                "email": each_user.email,
                "role": each_user.role,
                "temp_start": float(each_user.temp_start) if each_user.temp_start is not None else each_user.temp_start,
                "temp_end": float(each_user.temp_end) if each_user.temp_end is not None else each_user.temp_end
            }
            for each_user in db.session.query(User).order_by(User.username.asc()).paginate(page=page, per_page=limit).items
        ]

    @staticmethod
    def get_user_by_username(username: str):
        """Pass in a username and get that user if they exist (or else None)"""
        return db.session.query(User).filter(User.username == username).first()


@login.user_loader
def load_user(id: str) -> User:
    """
    Description
    -----------
    This function loads the user for a particular id

    Params
    ------
    :id: str
    Pass in the id as a string for a given user and this will return that user

    Return
    ------
    User object
    """
    return User.query.get(int(id))
