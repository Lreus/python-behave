Feature: Interact with kong software to perform authentication

Background:
  Given kong is accessible at "http://behave_kong:8001"

@wip
Scenario: Perform service creation
  Given there is no service named "my-custom-service"
  When I create a service named "my-custom-service" pointing to "http://www.google.com"
  And I request kong for service "my-custom-service"
  Then the request status code should be 200
  #And the response content should contain Json

