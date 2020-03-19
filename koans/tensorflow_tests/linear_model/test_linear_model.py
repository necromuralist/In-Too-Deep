# coding=utf-8
"""Testing the hello-world linear model."""

# from pypi
from expects import (
    be,
    contain_exactly,
    expect,
)

from pytest_bdd import (
    given,
    scenarios,
    then,
    when,
)

# thing under test TUT
from .solution import (
    compile_network,
    fit_model,
    make_model,
    predict,
    )

# for testing
from ..fixtures import katamari

And = when
and_also = then
scenarios("../../features/linear_model.feature")

# ******************** Imports ******************** #
# 'The modeler makes the imports'


@given('keras has been imported')
def patch_keras():
    return


@when('the mocks are in place')
def setup_mocks(katamari, mocker):
    manager = mocker.MagicMock()
    keras_mock = mocker.MagicMock()
    sequential = mocker.MagicMock()
    keras_mock.Sequential.return_value = sequential
    katamari.model = sequential
    dense = mocker.MagicMock()
    keras_mock.layers.Dense.return_value = dense
    
    manager.attach_mock(keras_mock.Sequential, "Sequential")
    manager.attach_mock(keras_mock.layers.Dense, "Dense")
    manager.attach_mock(sequential, "model")
    
    mocker.patch(f"{__package__}.solution.keras", keras_mock)
    katamari.expected_calls = [
        mocker.call.Sequential(),
        mocker.call.Dense(units=1, input_shape=[1]),
        mocker.call.model.add(dense)
    ]

    katamari.manager = manager
    katamari.keras = keras_mock
    return

@And("the modeler makes the network")
def make_network(katamari):
    katamari.actual_model = make_model()
    return


@then('the correct calls were made')
def check_the_calls(katamari):
    expect(katamari.manager.mock_calls).to(
        contain_exactly(*katamari.expected_calls))
    return

@and_also("the model was returned")
def check_model(katamari):
    expect(katamari.actual_model).to(be(katamari.model))
    return

# ********** Compile the Model ********** #
#  Scenario: The modeler compiles the network
#    Given the modeler made the network

@when("the compile mocks are in place")
def setup_expected_compile_call(katamari, mocker):
    katamari.expected_calls = katamari.expected_calls + [
        mocker.call.model.compile(optimizer="sgd",
                               loss="mean_squared_error")
    ]
    return

@when("the modeler compiles the network")
def call_compile_network(katamari, mocker):
    katamari.actual_model = compile_network()
    return


# Then the correct calls were made

# ********** Fit the Model ********** #
#  Scenario: The modeler fits the network
#    Given keras has been imported
#    When the mocks are in place
#    And the modeler compiles the network

@And("the fit mocks are in place")
def setup_fit_mocks(katamari, mocker):
    X = mocker.MagicMock()
    y = mocker.MagicMock()
    get_data = mocker.MagicMock()
    get_data.return_value = (X, y)
    mocker.patch(f"{__package__}.solution.get_data", get_data)

    katamari.expected_calls = katamari.expected_calls + [
        mocker.call.model.fit(X, y, epochs=500)
    ]
    return

@And("the modeler fits the model")
def fit_the_model(katamari, mocker):
    katamari.actual_model = fit_model()
    return

#    Then the correct calls were made

# ********** Make a Prediction ********** #
#  Scenario: The modeler makes a prediction
#    Given keras has been imported
#    When the mocks are in place
#    And the compile mocks are in place
#    And the fit mocks are in place


@And("the modeler makes a prediction")
def make_prediction(katamari, mocker):
    get_input = mocker.MagicMock()
    inputs = [100.0]
    get_input.return_value = inputs
    mocker.patch(f"{__package__}.solution.get_input", get_input)    
    prediction = predict()
    katamari.expected_calls += [
        mocker.call.model.predict(inputs)
    ]
    return

#    Then the correct calls were made
