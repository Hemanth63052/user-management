import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from scripts.db.pg.sql_schemas import Users, UserMetadata


class SQLQueries:
    """
    This class contains SQL queries for user management operations.
    It is used to interact with the PostgreSQL database.
    """

    @staticmethod
    def check_user_with_email(email: str) -> select:
        """
        SQL query to check if a user exists with the given email.

        :arg.
            email (str): The email of the user to check.
        :return:
            select: SQLAlchemy select query to check user existence.
        """
        query = select(Users).options(joinedload(Users.user_metadata)).join(UserMetadata, UserMetadata.user_id==Users.id).filter((Users.email == email))
        return query

    @staticmethod
    def get_user_metadata_by_reset_token(reset_token:str):
        now = datetime.datetime.now(datetime.timezone.utc)
        return select(UserMetadata).options(joinedload(UserMetadata.user)).join(Users, Users.id == UserMetadata.user_id).filter(UserMetadata.reset_password_token == reset_token, UserMetadata.reset_password_expires_at<now)

    @staticmethod
    def get_user_by_id(user_id):
        query = select(Users).options(joinedload(
            Users.user_metadata
        )).filter((Users.id == user_id))
        return query
