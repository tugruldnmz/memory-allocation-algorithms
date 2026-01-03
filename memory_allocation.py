import random
import time

MEMORY_SIZE = 100


class MemoryAllocator:
    def __init__(self):
        self.free_list = [[0, MEMORY_SIZE]]
        self.allocated = []
        self.last_index = 0  # for Next Fit

    def merge_free_list(self):
        self.free_list.sort()
        merged = []
        for block in self.free_list:
            if not merged or merged[-1][0] + merged[-1][1] != block[0]:
                merged.append(block)
            else:
                merged[-1][1] += block[1]
        self.free_list = merged

    def free(self, start, size):
        self.free_list.append([start, size])
        self.merge_free_list()

    # -------- Allocation Algorithms --------

    def allocate_best_fit(self, size):
        best = None
        for block in self.free_list:
            if block[1] >= size:
                if best is None or block[1] < best[1]:
                    best = block

        if best:
            start = best[0]
            best[0] += size
            best[1] -= size
            if best[1] == 0:
                self.free_list.remove(best)
            self.allocated.append((start, size))
            return start, size
        return None

    def allocate_worst_fit(self, size):
        worst = None
        for block in self.free_list:
            if block[1] >= size:
                if worst is None or block[1] > worst[1]:
                    worst = block

        if worst:
            start = worst[0]
            worst[0] += size
            worst[1] -= size
            if worst[1] == 0:
                self.free_list.remove(worst)
            self.allocated.append((start, size))
            return start, size
        return None

    def allocate_next_fit(self, size):
        n = len(self.free_list)
        for i in range(n):
            index = (self.last_index + i) % n
            block = self.free_list[index]
            if block[1] >= size:
                start = block[0]
                block[0] += size
                block[1] -= size
                if block[1] == 0:
                    self.free_list.remove(block)
                self.last_index = index
                self.allocated.append((start, size))
                return start, size
        return None


# -------- Experiments --------

def experiment_speed(allocator, allocate_func):
    start_time = time.time()
    allocated = []

    for _ in range(200):
        size = random.randint(1, 10)
        block = allocate_func(size)
        if block:
            allocated.append(block)

        if allocated:
            free_block = random.choice(allocated)
            allocated.remove(free_block)
            allocator.free(*free_block)

    return time.time() - start_time


if __name__ == "__main__":
    print("Speed Test Results\n")

    alloc = MemoryAllocator()
    t1 = experiment_speed(alloc, alloc.allocate_best_fit)
    print("Best Fit time:", t1)

    alloc = MemoryAllocator()
    t2 = experiment_speed(alloc, alloc.allocate_worst_fit)
    print("Worst Fit time:", t2)

    alloc = MemoryAllocator()
    t3 = experiment_speed(alloc, alloc.allocate_next_fit)
    print("Next Fit time:", t3)
