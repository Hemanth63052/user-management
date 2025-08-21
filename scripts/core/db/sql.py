from scripts.db.pg.queries import SQLQueries
from scripts.db.pg.ops import SQLOps
from scripts.db.pg.sql_schemas import Users, UserMetadata


class SQLHandler:
    """
    SQLHandler is a base class for handling SQL operations.
    It provides methods to execute SQL queries and manage database connections.
    """

    def __init__(self, session):
        self.sql_ops = SQLOps(session)

    async def check_user_exists_by_mail(self, email: str):
        """
        Check if a user exists with the given email.

        :param email: The email of the user to check.
        :return: True if the user exists, False otherwise.
        """
        query = SQLQueries.check_user_with_email(email)
        result = await self.sql_ops.execute_query(query=query, first_result=True)
        return result

    def insert_new_user(self, user_data: dict):
        """
        Insert a new user into the database.

        :param user_data: A dictionary containing user data.
        :return: The result of the insert operation.
        """
        return self.sql_ops.insert_one(user_data, model=Users)

    def insert_user_metadata(self, user_metadata: dict):
        """
        Insert user metadata into the database.

        :param user_metadata: A dictionary containing user metadata.
        :return: The result of the insert operation.
        """
        return self.sql_ops.insert_one(user_metadata, model=UserMetadata)

    def update_user(self, user_data: dict, filter_condition):
        """
        Update user data in the database.

        :param user_data: A dictionary containing user data to update.
        :param filter_condition: The condition to filter which user to update.
        :return: The result of the update operation.
        """
        return self.sql_ops.update_query(data=user_data, model=Users, filter_condition=filter_condition)

    def update_user_metadata(self, user_metadata: dict, filter_condition):
        """
        Update user metadata in the database.

        :param user_metadata: A dictionary containing user metadata to update.
        :param filter_condition: The condition to filter which user metadata to update.
        :return: The result of the update operation.
        """
        return self.sql_ops.update_query(data=user_metadata, model=UserMetadata, filter_condition=filter_condition)

    async def get_user_metadata(self, reset_token: str):
        """
        Get the user metadata from the database.

        :params filter_conditions: The condition to filter which user metadata to update.
        :return: The result of the operation.
        """
        query = SQLQueries.get_user_metadata_by_reset_token(reset_token)
        result = await self.sql_ops.execute_query(query=query)
        return result

    async def get_user_by_id(self, user_id: str):
        query = SQLQueries.get_user_by_id(user_id=user_id)
        result = await self.sql_ops.execute_query(query=query, json_result=True, first_result=True)
        return result

    async def get_user_metadata_by_verification_token(self, verification_token: str):
        """
        Get user metadata by verification token.

        :param verification_token: The token used for email verification.
        :return: The user metadata if found, otherwise None.
        """
        query = SQLQueries.get_user_metadata_by_verification_token(verification_token)
        result = await self.sql_ops.execute_query(query=query, first_result=True)
        return result

