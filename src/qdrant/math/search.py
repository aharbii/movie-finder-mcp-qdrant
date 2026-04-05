import math


def dot_product(v: list[float], w: list[float]) -> float:
    """
    Calculate the dot product of two vectors

    Args:
        v (list[float]): first vector
        w (list[float]): second vector

    Returns:
        float: dot product of the vectors
    """
    if len(v) != len(w):
        raise ArithmeticError("Dot product is only valid between vectors of the same dimension.")

    result: float = 0.0

    for i in range(len(v)):
        result += v[i] * w[i]

    return result


def magnitude(v: list[float]) -> float:
    """
    Calculate the magnitude of a vector

    Args:
        v (list[float]): vector

    Returns:
        float: magnitude of the vector
    """
    squared_sum = sum(math.pow(i, 2) for i in v)

    length = math.sqrt(squared_sum)
    return length


def cosine_similarity(v: list[float], w: list[float]) -> float:
    """
    Calculate cosine similarity between two vectors

    Args:
        v (list[float]): first vector
        w (list[float]): second vector

    Returns:
        float: cosine similarity value
    """
    dot = dot_product(v, w)

    v_mag = magnitude(v)
    w_mag = magnitude(w)

    similarity = dot / (v_mag * w_mag)
    return similarity
