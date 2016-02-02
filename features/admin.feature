Feature: admin script

    Background:
        Given the admin script
          And a username
          And a hostname
          And the database is reset


    Scenario: grant user access
        Given the server exists
          And the user exists
         When I grant the user access to the server
         Then the user has access to the server

    Scenario: revoke user access
        Given the server exists
          And the user exists
         When I grant the user access to the server
          And I revoke the user access from the server
         Then the user does not have access to the server