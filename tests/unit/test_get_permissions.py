from unittest.mock import patch

import pytest

from src.hardshell.linux import get_permissions as get_permissions_linux


# Mocked os.stat result
class MockStatResult:
    def __init__(self, mode):
        self.st_mode = mode


# Tests
@patch("os.stat")
def test_get_permissions(mock_stat):
    # Define the mock behavior
    mock_result = MockStatResult(mode=0o755)
    mock_stat.return_value = mock_result

    # Call the function
    path = "/fake/path"
    result = get_permissions_linux(path)

    # Assertions
    assert result.st_mode == 0o755
    mock_stat.assert_called_once_with(path)


@patch("os.stat", side_effect=FileNotFoundError)
def test_get_permissions_file_not_found(mock_stat):
    # Call the function with a path that raises FileNotFoundError
    path = "/non/existent/path"

    with pytest.raises(FileNotFoundError):
        get_permissions_linux(path)

    mock_stat.assert_called_once_with(path)


@patch("os.stat", side_effect=PermissionError)
def test_get_permissions_permission_denied(mock_stat):
    # Call the function with a path that raises PermissionError
    path = "/restricted/path"

    with pytest.raises(PermissionError):
        get_permissions_linux(path)

    mock_stat.assert_called_once_with(path)
