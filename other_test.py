from common.value_type import Point, Sample

from generator.plane_random_generator import PlaneRandomGenerator


if __name__ == "__main__":
    plane_random_gen = PlaneRandomGenerator()
    plane_random_gen._select_strategy = 'balanced random'

    plane_random_gen.set_data([], [
        Point(0.15, 0.15),
        Point(0.85, 0.15),
        Point(0.85, 0.85),
        Point(0.15, 0.85),
    ])

    batch_test = plane_random_gen.generate(10)

    for item in batch_test:
        print(item)


input = torch.Tensor([
    [0.2, 0.2],
    [0.8, 0.8],
    [0.8, 0.2],
    [0.2, 0.8],
    [0.1, 0.9],
    [0.1, 0.1],
    [0.9, 0.1],
    [0.9, 0.9],
    [0.28, 0.56],
])

target = torch.Tensor([
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    0,
])