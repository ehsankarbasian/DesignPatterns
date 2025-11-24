
# FlyWeight object
class KarakTea:
    pass


# FlyWeight Factory
class TeaMaker:
    
    _available_tea: dict = {}
    
    def make(self, preference):
        
        if preference not in self._available_tea:
            new_tea = KarakTea()
            print(f'Creating new tea: "{id(new_tea)}"')
            self._available_tea[preference] = new_tea
        
        return self._available_tea[preference]


# TeaClient
class TeaShop:
    
    _orders: dict = {}
    _tea_maker: TeaMaker
    
    def __init__(self, tea_maker: TeaMaker):
        self._tea_maker = tea_maker
    
    def take_order(self, tea_type: str, table: int):
        self._orders[table] = self._tea_maker.make(preference=tea_type)
    
    def serve(self):
        for table, tea in self._orders.items():
            print(f'Serving tea "{id(tea)}" to Table "{table}"')


if __name__ == "__main__":
    tea_maker = TeaMaker()
    shop = TeaShop(tea_maker)
    
    shop.take_order('less sugar', 1)
    shop.take_order('more milk', 2)
    shop.take_order('less sugar', 3)
    shop.take_order('more milk', 4)
    shop.take_order('without sugar', 5)
    shop.take_order('less sugar', 6)
    
    shop.serve()
