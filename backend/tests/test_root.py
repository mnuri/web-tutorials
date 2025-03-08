import service


# Function returns a dictionary with a "message" key
def test_returns_dictionary_with_message_key():
    # Arrange
    # No setup needed

    # Act
    result = service.root()

    # Assert
    assert "message" in result


# The value of the "message" key is "Hello World"
def test_message_value_is_hello_world():
    # Arrange
    # No setup needed

    # Act
    result = service.root()

    # Assert
    assert result["message"] == "Hello World"


# The function returns the expected data type (dictionary)
def test_returns_dictionary_type():
    # Arrange
    # No setup needed

    # Act
    result = service.root()

    # Assert
    assert isinstance(result, dict)


# The function requires no arguments to execute successfully
def test_requires_no_arguments():
    # Arrange
    # No setup needed

    # Act & Assert
    try:
        service.root()
        assert True  # If we get here, no exception was raised
    except TypeError:
        assert False, "Function should not require any arguments"


# Function behavior when called multiple times (should be consistent)
def test_consistent_behavior_on_multiple_calls():
    # Arrange
    # No setup needed

    # Act
    result1 = service.root()
    result2 = service.root()
    result3 = service.root()

    # Assert
    assert result1 == result2 == result3
    assert result1 is not result2  # Ensure they're different objects
    assert result2 is not result3  # Ensure they're different objects


# Memory usage when called in a loop many times
def test_memory_usage_in_loop():
    # Arrange
    import gc
    import sys

    # Force garbage collection to get a clean starting point
    gc.collect()
    initial_size = sys.getsizeof([])

    # Act
    results = []
    for _ in range(1000):
        results.append(service.root())

    # Assert
    # Check that memory usage is reasonable
    # Each dict should be small, so 1000 dicts shouldn't exceed 1MB
    memory_used = sys.getsizeof(results) - initial_size
    assert memory_used < 1_000_000, f"Memory usage too high: {memory_used} bytes"

    # Cleanup
    del results
    gc.collect()


# The function's return type matches the type annotation
def test_return_type_matches_annotation():
    # Arrange
    from typing import get_type_hints

    # Act
    result = service.root()
    type_hints = get_type_hints(service.root)
    return_type_hint = type_hints.get("return")

    # Assert
    # Check if the return type hint is dict[str, str]
    assert return_type_hint.__origin__ is dict
    assert return_type_hint.__args__ == (str, str)

    # Check if the actual return value matches the type hint
    assert isinstance(result, dict)
    for key, value in result.items():
        assert isinstance(key, str)
        assert isinstance(value, str)


# Immutability of the returned dictionary
def test_returned_dict_immutability():
    # Arrange
    original = service.root()
    modified = service.root()

    # Act
    modified["message"] = "Modified message"
    new_call_result = service.root()

    # Assert
    assert original["message"] == "Hello World"
    assert new_call_result["message"] == "Hello World"
    assert modified["message"] == "Modified message"
    assert original is not modified
    assert new_call_result is not original
    assert new_call_result is not modified
