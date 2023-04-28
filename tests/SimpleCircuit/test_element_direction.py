from CircuitCalculator.SimpleCircuit.Elements import get_node_direction
import schemdraw.util

def test_node_direction_identifies_positive_x_direction() -> None:
    n1 = schemdraw.util.Point([0, 0])
    n2 = schemdraw.util.Point([3, 0])

    dx, _ = get_node_direction(n1, n2)
    assert dx > 0

def test_node_direction_identifies_positive_y_direction() -> None:
    n1 = schemdraw.util.Point([0, 0])
    n2 = schemdraw.util.Point([0, 3])

    _, dy = get_node_direction(n1, n2)
    assert dy > 0

def test_node_direction_identifies_negative_x_direction() -> None:
    n1 = schemdraw.util.Point([3, 0])
    n2 = schemdraw.util.Point([0, 0])

    dx, _ = get_node_direction(n1, n2)
    assert dx < 0

def test_node_direction_identifies_negative_y_direction() -> None:
    n1 = schemdraw.util.Point([0, 3])
    n2 = schemdraw.util.Point([0, 0])

    _, dy = get_node_direction(n1, n2)
    assert dy < 0

def test_node_direction_identifies_equal_x_direction_as_positive() -> None:
    n1 = schemdraw.util.Point([0, 0])
    n2 = schemdraw.util.Point([0, 3])

    dx, _ = get_node_direction(n1, n2)
    assert dx > 0

def test_node_direction_identifies_equal_y_direction_as_positive() -> None:
    n1 = schemdraw.util.Point([0, 0])
    n2 = schemdraw.util.Point([3, 0])

    _, dy = get_node_direction(n1, n2)
    assert dy > 0