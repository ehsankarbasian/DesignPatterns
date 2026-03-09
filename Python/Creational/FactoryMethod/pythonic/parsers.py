
# Products
class JSONParser:
    def parse(self, text):
        print("Parsing JSON")

class XMLParser:
    def parse(self, text):
        print("Parsing XML")


PARSERS = {
        "json": JSONParser,
        "xml": XMLParser,
    }


# Factory
def create_parser(format):
    parser_class = PARSERS.get(format)

    if not parser_class:
        raise ValueError("Unsupported format")

    return parser_class()


# Client
parser = create_parser("json")
parser.parse("{}")
