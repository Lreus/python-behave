Feature: Interact with project databases

@wip
Scenario: test kong database connection
Given kong database is accessible over this psql configuration
  |key      |value          |
  |dbname   | behave_kong_db|
  |user     | behave_kong   |
  |password | kong          |
  |host     | behave_pgsql  |
  |port     | 5432          |