import pytest
from tracker_helpers import trilaterate_3d  # Replace 'your_module_name' with the actual module name

# Example test cases
@pytest.mark.parametrize("anchors, distances, expected_position", [
    (
        [(0, 0, 0), (5, 0, 0), (0, 5, 0)], 
        [2.5, 4.5, 3.5], 
        (1.4285714285714286, 1.4285714285714286, 1.6329931618554528)),  # Replace with your actual values
    # Add more test cases as needed
])
def test_trilaterate_3d(anchors, distances, expected_position):
    try:
        result = trilaterate_3d(*anchors, *distances)
        assert result == pytest.approx(expected_position, rel=1e-6)
    except ValueError:
        pytest.fail("ValueError not expected for valid input")

# def test_trilaterate_invalid_input():
#     with pytest.raises(ValueError):
#         # Invalid input values that should trigger a ValueError
#         trilaterate_3d((0, 0, 0), (0, 0, 0), (0, 0, 0), 0, 0, 0)

# Run the tests
if __name__ == "__main__":
    pytest.main()
