from backend.functions import auth

# Test the scope checking mechanism

def test_validate_scope_1():
    user_scope: int = 0b11
    requestor_scope: int = 0b10

    assert auth.validate_scope(user_scope,requestor_scope) == True

def test_validate_scope_2():
    user_scope: int = 0b01
    requestor_scope: int = 0b01

    assert auth.validate_scope(user_scope,requestor_scope) == True

def test_validate_scope_3():
    user_scope: int = 0b10
    requestor_scope: int = 0b01

    assert auth.validate_scope(user_scope,requestor_scope) == False


