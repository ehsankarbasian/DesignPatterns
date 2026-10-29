
# Products
class StripePayment:
    def pay(self, amount):
        print("Paying with Stripe")

class PayPalPayment:
    def pay(self, amount):
        print("Paying with PayPal")


PAYMENT_PROVIDERS = {
        "stripe": StripePayment,
        "paypal": PayPalPayment,
    }


# Factory method
def create_payment_provider(config):
    provider_name = config["payment_provider"]
    provider_class = PAYMENT_PROVIDERS[provider_name]
    return provider_class()


# Client
config = {"payment_provider": "stripe"}
provider = create_payment_provider(config)
provider.pay(100)
