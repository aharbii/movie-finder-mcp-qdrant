import pytest

from qdrant.math.search import cosine_similarity, dot_product, magnitude


def test_dot_product() -> None:
    assert dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == 32.0


def test_dot_product_mismatched_dimensions() -> None:
    with pytest.raises(ArithmeticError):
        dot_product([1.0], [1.0, 2.0])


def test_magnitude() -> None:
    assert magnitude([3.0, 4.0]) == 5.0


def test_cosine_similarity() -> None:
    v = [1.0, 0.0]
    w = [0.0, 1.0]
    assert cosine_similarity(v, w) == 0.0  # Orthogonal vectors

    v2 = [1.0, 1.0]
    w2 = [2.0, 2.0]
    assert cosine_similarity(v2, w2) == pytest.approx(1.0)  # Same direction vectors
