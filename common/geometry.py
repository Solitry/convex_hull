from typing import List

from .value_type import Point


def is_in_convex(point: Point, convex_points: List[Point]) -> bool:
    for index in range(len(convex_points)):
        next_index = (index + 1) % len(convex_points)

        convex_edge = convex_points[next_index] - convex_points[index]
        point_vector = point - convex_points[index]

        if (convex_edge ^ point_vector) < 0:
            return False
    
    return True


if __name__ == '__main__':
    test_convex_points = [
        Point(0.15, 0.15),
        Point(0.85, 0.15),
        Point(0.85, 0.85),
        Point(0.15, 0.85),
    ]

    print(is_in_convex(Point(0.41, 0.35), test_convex_points))  # in
    print(is_in_convex(Point(0.68, 0.48), test_convex_points))  # in
    print(is_in_convex(Point(0.51, 0.87), test_convex_points))  # out
    print(is_in_convex(Point(0.86, 0.51), test_convex_points))  # out
    print(is_in_convex(Point(0.95, 0.93), test_convex_points))  # out
