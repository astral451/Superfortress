"""Core simulation logic for Superfortress.

Deliberately has no dependency on Kivy or any rendering library, so it can
be imported and exercised in a plain Python REPL/test to verify the sim
runs correctly before ever touching a device.
"""
import random

TREE = "tree"
GRASS = "grass"
STONE = "stone"
WATER = "water"

TERRAIN_WEIGHTS = {
    GRASS: 55,
    TREE: 30,
    STONE: 10,
    WATER: 5,
}


class World:
    def __init__(self, width=16, height=12, seed=None):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.tiles = self._generate_terrain()
        self.wood = 0
        self.stone = 0
        self.tick_count = 0
        self.worker_x = width // 2
        self.worker_y = height // 2
        self.worker_target = None

    def _generate_terrain(self):
        terrains = list(TERRAIN_WEIGHTS.keys())
        weights = list(TERRAIN_WEIGHTS.values())
        return [
            [self.rng.choices(terrains, weights=weights, k=1)[0] for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def tile_at(self, x, y):
        return self.tiles[y][x]

    def _nearest_resource(self, kind):
        best = None
        best_dist = None
        for y in range(self.height):
            for x in range(self.width):
                if self.tiles[y][x] == kind:
                    dist = abs(x - self.worker_x) + abs(y - self.worker_y)
                    if best_dist is None or dist < best_dist:
                        best = (x, y)
                        best_dist = dist
        return best

    def _step_worker_toward(self, target):
        tx, ty = target
        if self.worker_x < tx:
            self.worker_x += 1
        elif self.worker_x > tx:
            self.worker_x -= 1
        elif self.worker_y < ty:
            self.worker_y += 1
        elif self.worker_y > ty:
            self.worker_y -= 1

    def tick(self):
        """Advance the simulation by one step. Returns True if the world
        state changed in a way that requires a redraw."""
        self.tick_count += 1
        changed = False

        if self.worker_target is None or self.tile_at(*self.worker_target) != TREE:
            self.worker_target = self._nearest_resource(TREE)

        if self.worker_target is None:
            return changed

        if (self.worker_x, self.worker_y) == self.worker_target:
            tx, ty = self.worker_target
            self.tiles[ty][tx] = GRASS
            self.wood += 1
            self.worker_target = None
            changed = True
        else:
            self._step_worker_toward(self.worker_target)
            changed = True

        return changed

    def trees_remaining(self):
        return sum(row.count(TREE) for row in self.tiles)


if __name__ == "__main__":
    world = World(seed=1)
    print(f"Start: {world.trees_remaining()} trees, wood={world.wood}")
    for _ in range(200):
        world.tick()
    print(f"After 200 ticks: {world.trees_remaining()} trees, wood={world.wood}, tick_count={world.tick_count}")
