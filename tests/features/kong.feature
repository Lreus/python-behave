Feature: Interact with kong software to perform authentication

Background:
  Given kong is accessible at "http://behave_kong:8001"

Scenario: Perform service creation
  Given there is no service named "my-custom-service"
  When I create a service named "my-custom-service" pointing to "http://www.google.com"
  And I request kong for service "my-custom-service"
  Then the request status code should be 200
  And the response content should contain Json
  And the response should have the matching key-values pairs
    |key     |value            |
    |name    |my-custom-service|
    |host    |www.google.com   |
    |protocol|http             |
    |port    |80               |

@wip
Scenario: Create an Oauth2 plugin enabled service
  Given there is no service named "behave-web"
  And there is a consumer identified by
  |username      |custom_id                           |
  |l.reus        |4fc4eae8-eb1e-4d9d-9d93-bcf46e49e8c0|

  When I create a service named "behave-web" pointing to "http://behave:5000"
  And I activate the oauth2 plugin for "behave-web" with these parameters
    |attribute                |value|
    |scopes                   |email|
    |mandatory_scope          |true |
    |enable_authorization_code|true |
  # Must ensure client_id is not a duplicate
  And I provision the current customer with these parameters
  |parameter      |value                       |
  |name           |Behave-Application          |
  |client_id      |l.reus@foo.com              |
  |client_secret  |dbdad115-2497-4fcb          |
  |redirect_uris  |http://behave:5000/logged_in|
