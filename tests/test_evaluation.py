from src.evaluation import adjusted_r2


def test_adjusted_r2_valid_range():
    value = adjusted_r2(0.8, n=100, p=5)
    assert value < 1
    assert value > -1
