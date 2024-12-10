import pytest

from sqlalchemy.exc import IntegrityError

from travel_buddy.travel_buddy.models.user_model import User


@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "password": "securepassword123"
    }


##########################################################
# User Creation
##########################################################

def test_create_user(session, sample_user):
    """Test creating a new user with a unique username."""
    User.create_user(**sample_user)
    user = session.query(User).filter_by(username=sample_user["username"]).first()
    assert user is not None, "User should be created in the database."
    assert user.username == sample_user["username"], "Username should match the input."
    assert len(user.salt) == 32, "Salt should be 32 characters (hex)."
    assert len(user.password) == 64, "Password should be a 64-character SHA-256 hash."

def test_create_duplicate_user(session, sample_user):
    """Test attempting to create a user with a duplicate username."""
    User.create_user(**sample_user)
    with pytest.raises(ValueError, match="User with username 'testuser' already exists"):
        User.create_user(**sample_user)
    
def test_username_case_sensitivity(session, sample_user):
    """Test whether usernames are case-insensitive."""
    User.create_user(**sample_user)
    with pytest.raises(ValueError, match="User with username 'testuser' already exists"):
        User.create_user(username="TestUser", password="anotherpassword")

def test_create_user_empty_fields(session):
    """Test creating a user with an empty username or password."""
    with pytest.raises(ValueError):
        User.create_user(username="", password="securepassword123")
    with pytest.raises(ValueError):
        User.create_user(username="testuser", password="")

##########################################################
# User Authentication
##########################################################

def test_check_password_correct(session, sample_user):
    """Test checking the correct password."""
    User.create_user(**sample_user)
    assert User.check_password(sample_user["username"], sample_user["password"]) is True, "Password should match."

def test_check_password_incorrect(session, sample_user):
    """Test checking an incorrect password."""
    User.create_user(**sample_user)
    assert User.check_password(sample_user["username"], "wrongpassword") is False, "Password should not match."

def test_check_password_user_not_found(session):
    """Test checking password for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.check_password("nonexistentuser", "password")

def test_password_hash_consistency(session, sample_user):
    """Test that the same password with a different salt results in a different hash."""
    User.create_user(**sample_user)
    user1 = session.query(User).filter_by(username=sample_user["username"]).first()
    User.create_user(username="testuser2", password=sample_user["password"])
    user2 = session.query(User).filter_by(username="testuser2").first()
    assert user1.password != user2.password, "Hashes should differ due to unique salts."

##########################################################
# Update Password
##########################################################

def test_update_password(session, sample_user):
    """Test updating the password for an existing user."""
    User.create_user(**sample_user)
    new_password = "newpassword456"
    User.update_password(sample_user["username"], new_password)
    assert User.check_password(sample_user["username"], new_password) is True, "Password should be updated successfully."

def test_update_password_user_not_found(session):
    """Test updating the password for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.update_password("nonexistentuser", "newpassword")


##########################################################
# Delete User
##########################################################

def test_delete_user(session, sample_user):
    """Test deleting an existing user."""
    User.create_user(**sample_user)
    User.delete_user(sample_user["username"])
    user = session.query(User).filter_by(username=sample_user["username"]).first()
    assert user is None, "User should be deleted from the database."

def test_delete_user_not_found(session):
    """Test deleting a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.delete_user("nonexistentuser")

