from typing import Optional, List

from .datamodel import UserDomainObject


class UserDataMapper:
    
    def __init__(self, database_connection):
        self.database_connection = database_connection


    def fetch_by_identifier(self, identifier: int) -> Optional[UserDomainObject]:
        query_text = f"SELECT id, name, email, is_active FROM users WHERE id = {identifier}"
        result = self.database_connection.connection.execute_query(query_text)
        if result is None:
            return None
        return UserDomainObject(
            identifier=result["id"],
            full_name=result["name"],
            email_address=result["email"],
            is_active=result["is_active"]
        )


    def fetch_all(self) -> List[UserDomainObject]:
        query_text = "SELECT id, name, email, is_active FROM users"
        results = self.database_connection.connection.execute_query(query_text)
        user_list = []
        for row in results:
            user_list.append(
                UserDomainObject(
                    identifier=row["id"],
                    full_name=row["name"],
                    email_address=row["email"],
                    is_active=row["is_active"]
                )
            )
        return user_list


    def insert(self, user_domain_object: UserDomainObject) -> int:
        query_text = (
            f"INSERT INTO users (name, email, is_active) "
            f"VALUES ('{user_domain_object.full_name}', '{user_domain_object.email_address}', {user_domain_object.is_active})"
        )
        self.database_connection.connection.execute_query(query_text)
        new_identifier = self.database_connection.last_insert_id
        return new_identifier


    def update(self, user_domain_object: UserDomainObject) -> None:
        query_text = (
            f"UPDATE users SET "
            f"name = '{user_domain_object.full_name}', "
            f"email = '{user_domain_object.email_address}', "
            f"is_active = {user_domain_object.is_active} "
            f"WHERE id = {user_domain_object.identifier}"
        )
        self.database_connection.connection.execute_query(query_text)
    
    
    def delete(self, identifier: int) -> None:
        query_text = f"DELETE FROM users WHERE id = {identifier}"
        self.database_connection.connection.execute_query(query_text)
