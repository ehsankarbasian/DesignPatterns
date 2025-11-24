from typing import Optional, List


# Domain object
class UserDomainObject:
    
    _id_: int
    _name: str
    _email: str
    
    def __init__(self, id_: Optional[int], name: str, email: str):
        self._id_ = id_
        self._name = name
        self._email = email
    
    @property
    def id_(self):
        return self._id_
    
    @id_.setter
    def id_(self, id_):
        self._id_ = id_
    
    @property
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email


# The ORM
class UserDataMapper:
    
    _db = ...
    
    def __init__(self, db):
        self._db = db
    
    
    def fetch_by_identifier(self, id_) -> Optional[UserDomainObject]:
        query = f'SELECT * FROM users WHERE id = {id_}'
        result = self._db.connection.execute_query(query)
        
        if result:
            return UserDomainObject(result['id_'], result['name'], result['email'])
        else:
            return None
    
    
    def insert(self, user: UserDomainObject) -> int:
        query = f'INSERT INTO users (name, email) VALUES ({user.name}, {user.email})'
        result = self._db.connection.execute_query(query)
        
        new_identifier = self._db.last_insert_id
        user.id_ = new_identifier
        return new_identifier
    
    
    def fetch_all(self) -> List[UserDomainObject]:
        query = f'SELECT * FROM users'
        results = self._db.connection.execute_query(query)
        
        user_list = []
        for row in results:
            user_list.append(UserDomainObject(row["id"], row["name"], row["email"]))
        
        return user_list


if __name__ == "__main__":
    db = ...
    user_mapper = UserDataMapper(db)

    user = user_mapper.fetch_by_identifier(id_=1)
    print(user.name)
    print(user.email)

    new_user = UserDomainObject(id_=None, name='ZoorAvar', email='Zoor@example.com')
    user_mapper.insert(new_user)
    
    user_mapper.fetch_all()
