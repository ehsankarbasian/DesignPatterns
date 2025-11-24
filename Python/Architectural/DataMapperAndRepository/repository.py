from typing import Optional, List

from .datamodel import UserDomainObject
from .data_mapper import UserDataMapper


class UserRepository:
    
    def __init__(self, user_data_mapper: UserDataMapper):
        self.user_data_mapper = user_data_mapper


    def get_by_identifier(self, identifier: int) -> Optional[UserDomainObject]:
        return self.user_data_mapper.fetch_by_identifier(identifier)


    def add(self, user_domain_object: UserDomainObject) -> None:
        identifier = self.user_data_mapper.insert(user_domain_object)
        user_domain_object.identifier = identifier


    def list_all(self) -> List[UserDomainObject]:
        return self.user_data_mapper.fetch_all()


    def list_active_users(self) -> List[UserDomainObject]:
        all_users = self.user_data_mapper.fetch_all()
        filtered_users = []
        for user in all_users:
            if user.is_active:
                filtered_users.append(user)
        return filtered_users


    def deactivate_user(self, identifier: int) -> None:
        user = self.user_data_mapper.fetch_by_identifier(identifier)
        if user is None:
            return
        user.is_active = False
        self.user_data_mapper.update(user)


    def update_email_address(self, identifier: int, new_email_address: str) -> None:
        user = self.user_data_mapper.fetch_by_identifier(identifier)
        if user is None:
            return
        user.email_address = new_email_address
        self.user_data_mapper.update(user)

    
    def delete_user(self, identifier: int) -> None:
        existing_user = self.user_data_mapper.fetch_by_identifier(identifier)
        
        if existing_user is None:
            return False
        
        self.user_data_mapper.delete(identifier)
        return True
