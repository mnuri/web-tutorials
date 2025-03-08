def root() -> dict[str, str]:
    return {"message": "Hello World"}


def say_hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}
