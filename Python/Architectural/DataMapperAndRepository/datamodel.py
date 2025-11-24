from typing import Optional


class UserDomainObject:
    
    def __init__(self, identifier: Optional[int],
                 full_name: str,
                 email_address: str,
                 is_active: bool = True
                 ):
        self.identifier = identifier
        self.full_name = full_name
        self.email_address = email_address
        self.is_active = is_active
