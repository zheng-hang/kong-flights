import bcrypt

# Example values
values = [
    (1, 'emily.jones987@example.org', 'abc123'),
    (2, 'sarah.smith5678@gmail.com', 'efg456'),
    (3, 'johndoe1234@example.com', 'hij789'),
    (4, 'alexander.wang4321@yahoo.com', 'klm135'),
    (5, 'lisa.brown2468@hotmail.com', 'opq246'),
    (6, 'michael.ng6543@example.net', 'rst357'),
    (7, 'sophia.wilson789@gmail.com', 'uvw468'),
    (8, 'daniel.kim321@example.com', 'xyz579')
]

# Generate salt and hash passwords
for pid, email, password in values:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    print(f"{pid},{email},{salt.decode()},{hashed_password.decode()}")

# def verify_password(original_password, hashed_password, salt):
#     # Hash the original password with the provided salt
#     hashed_original = bcrypt.hashpw(original_password.encode(), salt.encode())
#     # Check if the hashed passwords match
#     return hashed_original == hashed_password.encode()

# # Example usage
# pid = 1
# email = "emily.jones987@example.org"
# salt = "$2b$12$9WqKlzYKaHdX1Ul.QJHkHu"
# password_hash = "$2b$12$9WqKlzYKaHdX1Ul.QJHkHuXkiDOXexIKkvgRlOW6kApOChwjTa1ky"

# original_password = "abc123"
# result = verify_password(original_password, password_hash, salt)

# print(f"Password verification for PID {pid} ({email}): {result}")