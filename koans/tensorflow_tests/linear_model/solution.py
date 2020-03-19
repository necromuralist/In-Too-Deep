#+ Put the solutions here

# Imports
# python
import warnings
# pypi
with warnings.catch_warnings():
    # this is for the warnings that make the test
    # failures unreadable
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)    
    from tensorflow import keras

# The Fake Data
# The tests are using mocks so instead of using real data these will
# just be fakes
def get_data():
    return None, None


def get_input():
    return

# The code to implement
def make_model():
    """
    Make a dense model with one unit
    
    hint: the input shape will also be 1

    Returns:
     the model
    """
    model = keras.Sequential()
    dense = keras.layers.Dense(units=1, input_shape=[1])
    model.add(dense)
    return model


def compile_network():
    """
    compile the model using Stochastic Gradient Descent
     and measuring the loss with the Mean Squared Error

    Returns:
     the compiled model
    """
    model = make_model()
    model.compile(optimizer="sgd",
                  loss="mean_squared_error")
    return model

def fit_model():
    """Fit the model for 500 epochs

    Use X and y as defined above

    Returns:
     fitted model
    """
    X, y = get_data()
    model = compile_network()
    model.fit(X, y, epochs=500)
    return model

def predict():
    inputs = get_input()
    model = fit_model()
    model.predict(inputs)
    return
