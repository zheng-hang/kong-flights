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
    print(f"PID: {pid}, Email: {email}, Salt: {salt.decode()},{hashed_password.decode()}")