Feature: API

    Background:
        Given a username public key pair
          And a hostname port pair
          And an alias
          And the database is reset
        Given the server exists
          And the user exists

    Scenario: get a user by name
         When I access the user by name
         Then a valid User instance is returned

    Scenario: get a user's server list
         When I request the user's granted_servers list
         Then an empty list is returned

        Given the user has access to the server
         When I request the user's granted_servers list
         Then a valid list is returned
