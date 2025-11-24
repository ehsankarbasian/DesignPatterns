from .datamodel import UserDomainObject
from .data_mapper import UserDataMapper
from .repository import UserRepository


if __name__ == "__main__":
    database_connection = ...
    user_data_mapper = UserDataMapper(database_connection)
    user_repository = UserRepository(user_data_mapper)

    new_user = UserDomainObject(
        identifier=None,
        full_name="Example Name",
        email_address="example@example.com",
        is_active=True
    )
    user_repository.add(new_user)

    user_from_database = user_repository.get_by_identifier(new_user.identifier)

    user_repository.update_email_address(
        identifier=user_from_database.identifier,
        new_email_address="updated@example.com"
    )

    user_repository.deactivate_user(user_from_database.identifier)

    active_users = user_repository.list_active_users()
    all_users = user_repository.list_all()
    
    user_repository.delete_user(123)
