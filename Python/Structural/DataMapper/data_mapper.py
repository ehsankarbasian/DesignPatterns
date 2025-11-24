from typing import Optional


# Domain object
class User:
    
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
class UserMapper:
    
    _db = ...
    
    def __init__(self, db):
        self._db = db
    
    
    def get_by_id(self, id_) -> Optional[User]:
        query = f'SELECT * FROM users WHERE id = {id_}'
        result = self._db.connection.execute_query(query)
        
        if result:
            return User(result['id_'], result['name'], result['email'])
        else:
            return None
    
    
    def save(self, user: User) -> None:
        query = f'INSERT INTO users (name, email) VALUES ({user.name}, {user.email})'
        result = self._db.connection.execute_query(query)
        
        id_ = self._db.last_insert_id
        user.id_ = id_



if __name__ == "__main__":
    db = ...
    user_mapper = UserMapper(db)

    user = user_mapper.get_by_id(id_=1)
    print(user.name)
    print(user.email)

    new_user = User(id_=None, name='ZoorAvar', email='Zoor@example.com')
    user_mapper.save(new_user)
