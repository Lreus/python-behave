Feature: Interact with project databases

Scenario: test kong database connection
Given kong database is accessible over this psql configuration
  |key      | value         |
  |dbname   | behave_kong_db|
  |user     | behave_kong   |
  |password | kong          |
  |host     | behave_pgsql  |
  |port     | 5432          |

@database-cleanup
Scenario: Clean-up kong database
Given kong database is accessible over this psql configuration
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