#+ TITLE: pytest fixtures

# pypi
from pytest import fixture


class Katamari:
    """Stick things here

    This is to store values and pass them between the 'steps'
    """


@fixture
def katamari():
    """Creates the katamari object

    Example:

     def test_step(katamari):
         katamari.x = 5

     def test_x(katamari):
         expect(katamari.x).to(equal(5))

    Returns:
     Katamari object
    """
    k = Katamari()
    return k
