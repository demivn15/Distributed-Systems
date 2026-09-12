import ldap

def testLDAPAuthentication(serverInput: str, usernameInput: str, passwordInput: str) -> None:
    server: str = serverInput
    username: str = usernameInput
    password: str = passwordInput
    try:
        conn = ldap.initialize(server)
        conn.simple_bind_s(username, password)
        print(f"Authentication successful for: {username}")
        conn.unbind_s()
    except ldap.INVALID_CREDENTIALS:
        print(f"Authentication failed for {username}: Invalid credentials.")
    except Exception as error:
        print(f"Error: {error}")

def main() -> None:
    server: str = "ldap://localhost"
    print("--- Test Valid User and Password ---")
    validUserDN: str = "uid=user1234,ou=People,dc=alejandroydemian,dc=com"
    testLDAPAuthentication(server, validUserDN, "password123")
    print("\n--- Test Valid User with Invalid Password ---")
    testLDAPAuthentication(server, validUserDN, "wrongpassword123")
    print("\n--- Test Non-Existent User ---")
    invalidUserDN: str = "uid=nonexistentuser,ou=People,dc=alejandroydemian,dc=com"
    testLDAPAuthentication(server, invalidUserDN, "password123")

if __name__ == "__main__":
    main()
