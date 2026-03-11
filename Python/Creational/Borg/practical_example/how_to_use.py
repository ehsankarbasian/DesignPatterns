from threading import Thread

from config import Config


def demonstrate_shared_state():
    print("\n1. Shared state demonstration")
    config_a = Config()
    config_b = Config()

    print(f"Initial config_a: {config_a}")
    print(f"Initial config_b: {config_b}")

    # Change attributes on one instance
    config_a.debug = True
    config_a.db_url = "postgresql://prod:5432/app"

    print("\nAfter modifying config_a:")
    print(f"config_b.debug = {config_b.debug}  (shared)")
    print(f"config_b.db_url = {config_b.db_url}  (shared)")


def demonstrate_descriptor_access():
    print("\n2. Descriptor introspection via class")
    db_desc = Config.db_url            # Access descriptor directly
    print(f"Config.db_url is a {type(db_desc).__name__} (It is our descriptor)")
    print(f"Current value: {db_desc._value}")
    print(f"Default value: {db_desc.default}")


def demonstrate_reset():
    print("\n3. Reset values to default")
    config = Config()
    config.timeout = 60
    print(f"Before delete: config.timeout = {config.timeout}")
    del config.timeout
    print(f"After delete: config.timeout = {config.timeout} (The descriptor default value)")


def demonstrate_thread_safety():
    print("\n4. Thread-safe concurrent updates")

    config = Config()
    config.max_retries = 0

    def worker():
        for _ in range(1000):
            current = config.max_retries
            config.max_retries = current + 1

    threads = [Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Final max_retries: {config.max_retries}")
    print("Expected: ≈10 × 1000 = 10 000 (race-free if perfectly atomic)")


if __name__ == "__main__":
    demonstrate_shared_state()
    demonstrate_descriptor_access()
    demonstrate_reset()
    demonstrate_thread_safety()
