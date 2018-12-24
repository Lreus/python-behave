Feature: Interact with kong software to perform authentication

Background:
  Given kong is accessible at "http://behave_kong:8001"
  And kong database is accessible over this psql configuration
    |key      | value         |
    |dbname   | behave_kong_db|
    |user     | behave_kong   |
    |password | kong          |
    |host     | behave_pgsql  |
    |port     | 5432          |
  And I delete all oauth2 credentials
  And I delete all plugins
  And I delete all consumers
  And I delete all services

Scenario: Perform service creation
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


Scenario: Create an Oauth2 plugin enabled service
  When I create a service named "behave-web" pointing to "http://behave:5000"
  And I activate the oauth2 plugin for "behave-web" with these parameters
    |attribute                |value|
    |scopes                   |email|
    |mandatory_scope          |true |
    |enable_authorization_code|true |
  And I create a consumer named "l.reus" with id "4fc4eae8-eb1e-4d9d-9d93-bcf46e49e8c0"
  And I provision the current consumer with these parameters
  |parameter      |value                       |
  |name           |Behave-Application          |
  |client_id      |l.reus@foo.com              |
  |client_secret  |dbdad115-2497-4fcb          |
  |redirect_uris  |http://behave:5000/logged_in|
