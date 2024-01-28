# https://stackoverflow.com/questions/19053707/converting-snake-case-to-lower-camel-case-lowercamelcase

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


if __name__ == "__main__":
    var = "snake_case"
    print(to_camel_case(var))
