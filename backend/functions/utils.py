def is_folder_name_allowed(name: str) -> bool:
    """
    Check if the folder name is allowed.
    :param name: Folder name to check.
    :return: True if the folder name is allowed, False otherwise.
    """
    if name is None or name == "":
        return False

    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if any(char in name for char in invalid_chars):
        return False

    if len(name) > 20:
        return False

    return True