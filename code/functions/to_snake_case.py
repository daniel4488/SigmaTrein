# https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case?rq=3

import re


def to_snake_case(camel_str: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


if __name__ == "__main__":
    var = "CamelCase"
    print(to_snake_case(var))
