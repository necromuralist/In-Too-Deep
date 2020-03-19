Feature: A Linear Model
  As a modeler I want to be able to create a linear model using tensorflow.
            
  Scenario: The modeler defines the network
    Given keras has been imported
    When the mocks are in place
    And the modeler makes the network
    Then the correct calls were made
    And the model was returned

  Scenario: The modeler compiles the network
    Given keras has been imported
    When the mocks are in place
    And the compile mocks are in place
    And the modeler compiles the network
    Then the correct calls were made
    And the model was returned

  Scenario: The modeler fits the network
    Given keras has been imported
    When the mocks are in place
    And the compile mocks are in place
    And the fit mocks are in place
    And the modeler fits the model
    Then the correct calls were made

  Scenario: The modeler makes a prediction
    Given keras has been imported
    When the mocks are in place
    And the compile mocks are in place
    And the fit mocks are in place
    And the modeler makes a prediction
    Then the correct calls were made
