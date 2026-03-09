
# Products
class LocalStorage:
    def save(self, file):
        print("Saving locally ...")

class ServerStorage:
    def save(self, file):
        print("Saving to Server ...")

class LocalLogger:
    pass

class CloudLogger:
    pass


# Concrete factories
class LocalFactory:
    storage = LocalStorage
    logger = LocalLogger

class CloudFactory:
    storage = ServerStorage
    logger = CloudLogger


# Register factories
FACTORIES = {
        "local": LocalFactory,
        "cloud": CloudFactory,
    }


# Client
def get_factory(env: str):
    return FACTORIES[env]

factory = get_factory("cloud")

storage = factory.storage().save('file_name')
logger = factory.logger()
