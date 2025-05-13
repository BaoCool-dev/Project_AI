from queue import Queue, PriorityQueue
import random
import math
import copy
import numpy as np
from collections import deque
import time

class algorithm:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    def list_to_tuple_state(self, flat_state):
        """Chuyển đổi danh sách phẳng thành tuple của tuple."""
        if len(flat_state) != 9:
            raise ValueError("Invalid state length")
        return tuple(tuple(flat_state[i * 3:(i + 1) * 3]) for i in range(3))

    def tuple_to_list_state(self, tuple_state):
        """Chuyển đổi tuple của tuple thành danh sách phẳng."""
        return [num for row in tuple_state for num in row]

    def is_goal(self, state):
        """Kiểm tra xem trạng thái có phải là trạng thái mục tiêu hay không."""
        goal_state = self.goal_state
        if isinstance(state, tuple):  # Nếu là tuple của tuple
            state = self.tuple_to_list_state(state)
            goal_state = self.tuple_to_list_state(self.list_to_tuple_state(goal_state))
        return state == goal_state

    def get_successors(self, state):
        """Tạo danh sách các trạng thái kế tiếp."""
        is_tuple = isinstance(state, tuple)
        if is_tuple:
            state = self.tuple_to_list_state(state)
        
        if len(state) != 9 or sorted(state) != list(range(9)):
            raise ValueError("Invalid state: Must contain exactly numbers 0 to 8.")
        idx = state.index(0)
        row, col = divmod(idx, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
        successors = []
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                new_state = state[:]
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                successors.append(self.list_to_tuple_state(new_state) if is_tuple else new_state)
        return successors

    def is_solvable(self, state):
        """Kiểm tra xem trạng thái có thể giải được hay không."""
        if isinstance(state, tuple):
            state = self.tuple_to_list_state(state)
        inversions = 0
        state_without_zero = [x for x in state if x != 0]
        for i in range(len(state_without_zero)):
            for j in range(i + 1, len(state_without_zero)):
                if state_without_zero[i] > state_without_zero[j]:
                    inversions += 1
        return inversions % 2 == 0

    def heuristic(self, state):
        """Tính heuristic Manhattan."""
        if isinstance(state, tuple):
            state = self.tuple_to_list_state(state)
        goal_position = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1),
                        6: (1, 2), 7: (2, 0), 8: (2, 1), 0: (2, 2)}
        return sum(abs(r - goal_position[val][0]) + abs(c - goal_position[val][1])
                for val, (r, c) in [(state[i], divmod(i, 3)) for i in range(9)])

    def hamming_distance(self, state):
        """Calculates Hamming distance."""
        distance = 0
        for i in range(9):
            if state[i] != 0 and state[i] != self.goal_state[i]:
                distance += 1
        return distance

    def bfs(self, timeout=10.0):
        """Breadth-First Search."""
        start_time = time.time()
        queue = Queue()
        queue.put((self.initial_state, []))
        visited = {tuple(self.initial_state)}
        explored_states = [self.initial_state]
        while not queue.empty():
            if time.time() - start_time > timeout:
                return None, explored_states
            state, path = queue.get()
            if self.is_goal(state):
                return path + [state], explored_states
            for successor in self.get_successors(state):
                if tuple(successor) not in visited:
                    visited.add(tuple(successor))
                    queue.put((successor, path + [successor]))
                    explored_states.append(successor)
        return None, explored_states

    def dfs(self, timeout=30.0, max_depth=20):
        start_time = time.time()
        stack = [(self.initial_state, [], 0)]  # Thêm độ sâu vào stack
        visited = {tuple(self.initial_state)}
        explored_states = [self.initial_state]
        while stack:
            if time.time() - start_time > timeout:
                return None, explored_states
            state, path, depth = stack.pop()
            if self.is_goal(state):
                return path + [state], explored_states
            if depth < max_depth:  # Kiểm tra độ sâu
                for neighbor in self.get_successors(state):
                    if tuple(neighbor) not in visited:
                        visited.add(tuple(neighbor))
                        stack.append((neighbor, path + [state], depth + 1))
                        explored_states.append(neighbor)
        return None, explored_states

    def ucs(self, timeout=10.0):
        """Uniform Cost Search."""
        start_time = time.time()
        queue = PriorityQueue()
        queue.put((0, self.initial_state, []))
        visited = set()
        explored_states = [self.initial_state]
        while not queue.empty():
            if time.time() - start_time > timeout:
                return None, explored_states
            cost, state, path = queue.get()
            if self.is_goal(state):
                return path + [state], explored_states
            if tuple(state) not in visited:
                visited.add(tuple(state))
                for successor in self.get_successors(state):
                    queue.put((cost + 1, successor, path + [successor]))
                    explored_states.append(successor)
        return None, explored_states

    def ids(self, timeout=10.0):
        """Iterative Deepening Search."""
        start_time = time.time()
        depth = 0
        explored_states = []
        while True:
            if time.time() - start_time > timeout:
                return None, explored_states
            solution, sub_explored = self._dls(self.initial_state, [], set(), depth)
            explored_states.extend(sub_explored)
            if solution:
                return solution, explored_states
            depth += 1

    def _dls(self, state, path, visited, depth_limit):
        """Depth-Limited Search helper for IDS."""
        explored_states = [state]
        if self.is_goal(state):
            return path + [state], explored_states
        if depth_limit == 0:
            return None, explored_states
        visited.add(tuple(state))
        for successor in self.get_successors(state):
            if tuple(successor) not in visited:
                solution, sub_explored = self._dls(successor, path + [successor], visited, depth_limit - 1)
                explored_states.extend(sub_explored)
                if solution:
                    return solution, explored_states
        visited.remove(tuple(state))
        return None, explored_states

    def a_star(self, timeout=10.0):
        """A* Search."""
        start_time = time.time()
        queue = PriorityQueue()
        queue.put((self.heuristic(self.initial_state), self.initial_state, []))
        visited = set()
        explored_states = [self.initial_state]
        while not queue.empty():
            if time.time() - start_time > timeout:
                return None, explored_states
            _, state, path = queue.get()
            if self.is_goal(state):
                return path + [state], explored_states
            if tuple(state) not in visited:
                visited.add(tuple(state))
                for successor in self.get_successors(state):
                    f_cost = len(path) + 1 + self.heuristic(successor)
                    queue.put((f_cost, successor, path + [successor]))
                    explored_states.append(successor)
        return None, explored_states

    def ida_star(self, timeout=10.0):
        """IDA* Search."""
        start_time = time.time()
        threshold = self.heuristic(self.initial_state)
        explored_states = []
        while True:
            if time.time() - start_time > timeout:
                return None, explored_states
            solution, new_threshold = self._ida_dls(self.initial_state, [], set(), threshold, explored_states)
            if solution:
                return solution, explored_states
            if new_threshold == float("inf"):
                return None, explored_states
            threshold = new_threshold

    def _ida_dls(self, state, path, visited, threshold, explored_states):
        """Depth-Limited Search helper for IDA*."""
        explored_states.append(state)
        f_value = len(path) + self.heuristic(state)
        if f_value > threshold:
            return None, f_value
        if self.is_goal(state):
            return path + [state], None
        visited.add(tuple(state))
        min_threshold = float("inf")
        for successor in self.get_successors(state):
            if tuple(successor) not in visited:
                solution, new_threshold = self._ida_dls(successor, path + [successor], visited, threshold, explored_states)
                if solution:
                    return solution, None
                if new_threshold is not None:
                    min_threshold = min(min_threshold, new_threshold)
        visited.remove(tuple(state))
        return None, min_threshold

    def greedy_search(self, timeout=10.0):
        """Greedy Best-First Search."""
        start_time = time.time()
        queue = PriorityQueue()
        queue.put((self.heuristic(self.initial_state), self.initial_state, []))
        visited = set()
        explored_states = [self.initial_state]
        while not queue.empty():
            if time.time() - start_time > timeout:
                return None, explored_states
            _, state, path = queue.get()
            if self.is_goal(state):
                return path + [state], explored_states
            if tuple(state) not in visited:
                visited.add(tuple(state))
                for successor in self.get_successors(state):
                    queue.put((self.heuristic(successor), successor, path + [successor]))
                    explored_states.append(successor)
        return None, explored_states

    def simple_hill_climbing(self, timeout=10.0):
        """Simple Hill Climbing."""
        start_time = time.time()
        current_state = self.initial_state[:]
        path = [current_state]
        explored_states = [current_state]
        while True:
            if time.time() - start_time > timeout:
                return None, explored_states
            successors = self.get_successors(current_state)
            next_state = min(successors, key=self.heuristic, default=None)
            explored_states.extend(successors)
            if next_state is None or self.heuristic(next_state) >= self.heuristic(current_state):
                return None, explored_states
            current_state = next_state
            path.append(current_state)
            if self.is_goal(current_state):
                return path, explored_states

    def steepest_ascent_hill_climbing(self, timeout=10.0):
        """Steepest Ascent Hill Climbing."""
        start_time = time.time()
        current_state = self.initial_state[:]
        path = [current_state]
        explored_states = [current_state]
        while True:
            if time.time() - start_time > timeout:
                return None, explored_states
            successors = self.get_successors(current_state)
            next_state = min(successors, key=self.heuristic, default=None)
            explored_states.extend(successors)
            if next_state is None or self.heuristic(next_state) >= self.heuristic(current_state):
                return None, explored_states
            current_state = next_state
            path.append(current_state)
            if self.is_goal(current_state):
                return path, explored_states

    def random_hill_climbing(self, timeout=10.0):
        """Random Hill Climbing."""
        start_time = time.time()
        current_state = self.initial_state[:]
        path = [current_state]
        explored_states = [current_state]
        max_steps = 1000
        steps = 0
        while not self.is_goal(current_state) and steps < max_steps:
            if time.time() - start_time > timeout:
                return None, explored_states
            successors = self.get_successors(current_state)
            next_state = random.choice(successors)
            explored_states.extend(successors)
            if self.heuristic(next_state) < self.heuristic(current_state):
                current_state = next_state
                path.append(current_state)
            steps += 1
        return path if self.is_goal(current_state) else None, explored_states

    def simulated_annealing(self, timeout=10.0):
        """Simulated Annealing."""
        start_time = time.time()
        current_state = self.initial_state[:]
        path = [current_state]
        explored_states = [current_state]
        T = 1000.0
        T_min = 0.01
        alpha = 0.99
        max_steps = 50000
        for step in range(max_steps):
            if time.time() - start_time > timeout:
                return None, explored_states
            if self.is_goal(current_state):
                return path, explored_states
            successors = self.get_successors(current_state)
            if not successors:
                break
            next_state = random.choice(successors)
            explored_states.append(next_state)
            delta_E = self.heuristic(current_state) - self.heuristic(next_state)
            if delta_E > 0 or random.random() < math.exp(delta_E / T):
                current_state = next_state
                path.append(current_state)
            T *= alpha
            if T < T_min:
                break
        return path if self.is_goal(current_state) else None, explored_states

    def beam_search(self, timeout=10.0, k=2):
        """Beam Search with beam width k."""
        start_time = time.time()
        from heapq import heappush, heappop
        beam = [(self.heuristic(self.initial_state), self.initial_state[:], [])]
        explored_states = [self.initial_state]
        while beam:
            if time.time() - start_time > timeout:
                return None, explored_states
            new_beam = []
            for _, state, path in beam:
                if self.is_goal(state):
                    return path + [state], explored_states
                for succ in self.get_successors(state):
                    heappush(new_beam, (self.heuristic(succ), succ, path + [succ]))
                    explored_states.append(succ)
            beam = [heappop(new_beam) for _ in range(min(k, len(new_beam)))]
        return None, explored_states

    def and_or_search(self, timeout=10.0):
        """And-Or Tree Search with Iterative Deepening."""
        start_time = time.time()

        # Kiểm tra tính khả giải của trạng thái ban đầu
        if not self.is_solvable(self.initial_state):
            print("Initial state is not solvable")
            return None, []

        # Chuyển initial_state sang tuple để nhất quán
        initial_state = self.list_to_tuple_state(self.initial_state) if isinstance(self.initial_state,
                                                                                   list) else self.initial_state

        def explore(state, path, visited, depth_limit):
            """Khám phá trạng thái với giới hạn độ sâu."""
            if time.time() - start_time > timeout:
                return None, explored_states
            explored_states.add(state)  # Sử dụng set để tránh trùng lặp
            if self.is_goal(state):
                return path + [state], explored_states
            if depth_limit == 0:
                return None, explored_states
            visited.add(state)  # Trạng thái đã là tuple
            for succ in self.get_successors(state):
                if succ not in visited:
                    solution, sub_explored = explore(succ, path + [succ], visited, depth_limit - 1)
                    explored_states.update(sub_explored)
                    if solution:
                        return solution, explored_states
            visited.remove(state)
            return None, explored_states

        # Iterative Deepening
        depth = 0
        explored_states = set()  # Sử dụng set để tối ưu bộ nhớ
        while True:
            if time.time() - start_time > timeout:
                print("Timeout reached")
                return None, list(explored_states)
            print(f"Exploring depth: {depth}")
            solution, sub_explored = explore(initial_state, [], set(), depth)
            explored_states.update(sub_explored)
            if solution:
                print(f"Solution found at depth {depth}")
                return solution, list(explored_states)
            depth += 1
            # Giới hạn độ sâu tối đa để tránh chạy quá lâu
            if depth > 100:  # Có thể điều chỉnh
                print("Max depth reached")
                return None, list(explored_states)

    def genetic_algorithm(self, timeout=10.0):
        """Genetic Algorithm for 8-puzzle."""
        start_time = time.time()
        population_size = 100
        generations = 500
        mutation_rate = 0.2
        explored_states = []

        def create_individual():
            state = self.initial_state[:]
            for _ in range(5):
                successors = self.get_successors(state)
                state = random.choice(successors) if successors else state
            return state, []

        def crossover(parent1, parent2):
            split = random.randint(0, 8)
            child = parent1[:split] + parent2[split:]
            missing = [x for x in range(9) if x not in child]
            used = set(child)
            for i in range(9):
                if child.count(child[i]) > 1 or child[i] not in range(9):
                    child[i] = missing.pop(0)
            return child

        def mutate(individual):
            if random.random() < mutation_rate:
                successors = self.get_successors(individual)
                return random.choice(successors) if successors else individual
            return individual

        population = [create_individual() for _ in range(population_size)]
        explored_states.extend([ind[0] for ind in population])
        for generation in range(generations):
            if time.time() - start_time > timeout:
                return None, explored_states
            population.sort(key=lambda x: self.heuristic(x[0]))
            if self.is_goal(population[0][0]):
                path = population[0][1] + [population[0][0]]
                return path, explored_states
            new_population = population[:10]
            while len(new_population) < population_size:
                parent1, _ = random.choice(population[:20])
                parent2, _ = random.choice(population[:20])
                child = crossover(parent1, parent2)
                child = mutate(child)
                path = new_population[-1][1] + [child] if new_population else [child]
                new_population.append((child, path))
                explored_states.append(child)
            population = new_population
        best_individual, path = population[0]
        return path + [best_individual] if self.is_goal(best_individual) else None, explored_states

    def bfs_for_belief(self, start_state, max_depth=10):
        """Chạy BFS để tìm các trạng thái lân cận trong max_depth bước."""
        start_state = self.list_to_tuple_state(start_state) if isinstance(start_state, list) else start_state
        queue = deque([(start_state, 0)])
        visited = {start_state}
        states = set()

        while queue and len(states) < 5:
            state, depth = queue.popleft()
            if depth < max_depth:
                for neighbor in self.get_successors(state):
                    if tuple(neighbor) not in visited:
                        visited.add(tuple(neighbor))
                        queue.append((neighbor, depth + 1))
                        states.add(neighbor)
        return list(states)
    def optimized_bfs_for_belief(self, start_state, max_depth=1):
        """Tối ưu hóa BFS để tìm các trạng thái lân cận tốt nhất theo heuristic."""
        start_state = self.list_to_tuple_state(start_state) if isinstance(start_state, list) else start_state
        queue = deque([(start_state, 0)])
        visited = {start_state}
        states = [(self.heuristic(start_state), start_state)]

        while queue:
            state, depth = queue.popleft()
            if depth < max_depth:
                for neighbor in self.get_successors(state):
                    if tuple(neighbor) not in visited:
                        visited.add(tuple(neighbor))
                        queue.append((neighbor, depth + 1))
                        states.append((self.heuristic(neighbor), neighbor))

        states.sort()
        return {state for _, state in states[:10]}
    def get_observation(self, state):
        """Trả về vị trí (row, col) của ô số 1."""
        state = self.tuple_to_list_state(state) if isinstance(state, tuple) else state
        for i in range(9):
            if state[i] == 1:
                row, col = divmod(i, 3)
                return (row, col)
        return None
    def find_states_with_one_at_00(self, start_state, max_states=3):
        """Tìm các trạng thái có số 1 ở vị trí (0,0)."""
        start_state = self.list_to_tuple_state(start_state) if isinstance(start_state, list) else start_state
        queue = deque([(start_state, [])])
        visited = {start_state}
        states_with_one_at_00 = []

        while queue and len(states_with_one_at_00) < max_states:
            state, path = queue.popleft()
            if self.get_observation(state) == (0, 0) and self.is_solvable(state):
                states_with_one_at_00.append(state)
            for neighbor in self.get_successors(state):
                if tuple(neighbor) not in visited:
                    visited.add(tuple(neighbor))
                    queue.append((neighbor, path + [state]))

        while len(states_with_one_at_00) < max_states:
            numbers = list(range(9))
            random.shuffle(numbers)
            numbers[0] = 1
            remaining_numbers = [num for num in numbers[1:] if num != 1]
            if len(remaining_numbers) < 8:
                remaining_numbers.append(0)
            numbers = [1] + remaining_numbers[:8]
            state = self.list_to_tuple_state(numbers)
            if self.is_solvable(state) and state not in states_with_one_at_00:
                states_with_one_at_00.append(state)

        return states_with_one_at_00[:max_states]
    

    def bfs_for_belief(self, start_state, max_depth=10):
        """Chạy BFS để tìm các trạng thái lân cận trong max_depth bước."""
        start_state = self.list_to_tuple_state(start_state) if isinstance(start_state, list) else start_state
        queue = deque([(start_state, 0)])
        visited = {start_state}
        states = set()

        while queue and len(states) < 3:  # Chỉ cần 3 trạng thái
            state, depth = queue.popleft()
            if depth < max_depth:
                for neighbor in self.get_successors(state):
                    if tuple(neighbor) not in visited and self.is_solvable(neighbor):
                        visited.add(tuple(neighbor))
                        queue.append((neighbor, depth + 1))
                        states.add(neighbor)

        # Nếu không đủ 3 trạng thái, tạo ngẫu nhiên các trạng thái hợp lệ
        while len(states) < 3:
            numbers = list(range(9))
            random.shuffle(numbers)
            state = self.list_to_tuple_state(numbers)
            if tuple(state) not in visited and self.is_solvable(state):
                states.add(state)
                visited.add(tuple(state))

        return list(states)[:3]

    def partial_observable_search(self, initial_belief, timeout=10.0):
        """Tìm kiếm Partial Observable với số 1 ở (0,0)."""
        start_time = time.time()
        if not initial_belief or len(initial_belief) != 3 or not all(self.get_observation(state) == (0, 0) for state in initial_belief):
            return None, [], 0

        initial_belief = [self.list_to_tuple_state(state) if isinstance(state, list) else state for state in initial_belief]
        queue = deque([(set(initial_belief), [], 0)])
        visited = set()
        explored_states = list(initial_belief)
        belief_states_path = [list(initial_belief)]
        max_steps = 1000

        while queue and len(queue) < max_steps:
            if time.time() - start_time > timeout:
                return belief_states_path, explored_states, 0
            belief_state, path, steps = queue.popleft()
            belief_state_tuple = frozenset(belief_state)
            explored_states.extend(belief_state)

            if all(self.is_goal(state) for state in belief_state):
                total_steps = steps
                belief_states_path.append([self.list_to_tuple_state(self.goal_state)] * 3)
                return belief_states_path, explored_states, total_steps

            if belief_state_tuple in visited:
                continue
            visited.add(belief_state_tuple)

            for action in range(4):
                new_belief = set()
                for state in belief_state:
                    neighbors = self.get_successors(state)
                    if action < len(neighbors):
                        next_state = neighbors[action]
                        if self.get_observation(next_state) == (0, 0):
                            new_belief.add(next_state)
                        if random.random() < 0.1:
                            next_neighbors = self.get_successors(next_state)
                            uncertain_states = [s for s in next_neighbors if self.get_observation(s) == (0, 0)]
                            if uncertain_states:
                                uncertain_state = random.choice(uncertain_states)
                                new_belief.add(uncertain_state)
                    else:
                        new_belief.add(state)

                if new_belief:
                    new_belief = set(sorted(new_belief, key=self.heuristic)[:3])
                    queue.append((new_belief, path + [min(belief_state, key=self.heuristic)], steps + 1))
                    belief_states_path.append(list(new_belief))

        return None, explored_states, 0

    def belief_state_search(self, initial_belief, timeout=10.0):
        """Tìm kiếm Belief State với tối đa 5 trạng thái, mô phỏng độ phức tạp giống POS."""
        start_time = time.time()

        # Kiểm tra và log giá trị của initial_belief
        print(f"Initial belief in belief_state_search: {initial_belief}")
        if not isinstance(initial_belief, (list, tuple, set)) or not initial_belief or len(initial_belief) != 3:
            print(f"Error: initial_belief is invalid: {initial_belief}")
            return None, [], 0

        # Chuyển đổi initial_belief sang tuple của tuple
        try:
            initial_belief = [self.list_to_tuple_state(state) if isinstance(state, list) else state for state in
                              initial_belief]
        except Exception as e:
            print(f"Error converting initial_belief: {str(e)}")
            return None, [], 0

        initial_belief = set(initial_belief)
        explored = set(initial_belief)
        num_explored_states = len(initial_belief)
        belief_states_path = [list(initial_belief)]
        total_steps = 0
        visited = set()

        queue = deque([(initial_belief, [], 0)])
        while queue:
            if time.time() - start_time > timeout:
                print("Timeout reached")
                return belief_states_path, list(explored), total_steps
            belief_state, path, steps = queue.popleft()
            print(f"Processing belief_state: {belief_state}, Step: {steps}")
            belief_state_tuple = frozenset(belief_state)

            if belief_state_tuple in visited:
                continue
            visited.add(belief_state_tuple)

            # Yêu cầu tất cả trạng thái đạt mục tiêu, giống POS
            if all(self.is_goal(state) for state in belief_state):
                total_steps = steps
                belief_states_path.append([self.list_to_tuple_state(self.goal_state)] * len(initial_belief))
                print(f"Solution found at step {total_steps}")
                return belief_states_path, list(explored), total_steps

            for action in range(4):
                new_belief = set()
                for state in belief_state:
                    if not isinstance(state, tuple):
                        print(f"Error: Invalid state in belief_state: {state}")
                        continue
                    neighbors = self.get_successors(state)
                    if not isinstance(neighbors, (list, tuple)):
                        print(f"Error: get_successors returned invalid value: {neighbors}")
                        continue
                    if action < len(neighbors):
                        next_state = neighbors[action]
                        new_belief.add(next_state)
                        # Thêm uncertainty giống POS
                        if random.random() < 0.1:
                            next_neighbors = self.get_successors(next_state)
                            if next_neighbors and isinstance(next_neighbors, (list, tuple)):
                                uncertain_state = random.choice(next_neighbors)
                                if self.is_solvable(uncertain_state):
                                    new_belief.add(uncertain_state)

                if new_belief:
                    # Tăng giới hạn belief state lên 5 để tăng độ phức tạp
                    new_belief = set(sorted(new_belief, key=self.heuristic)[:5])
                    print(
                        f"New belief size: {len(new_belief)}, Heuristic avg: {sum(self.heuristic(s) for s in new_belief) / len(new_belief) if new_belief else 0}")
                    for state in new_belief:
                        if state not in explored:
                            explored.add(state)
                            num_explored_states += 1
                    if not isinstance(path, list):
                        print(f"Error: Path is not a list: {path}")
                        path = []
                    min_state = min(belief_state, key=self.heuristic)
                    queue.append((new_belief, path + [min_state], steps + 1))
                    belief_states_path.append(list(new_belief))

        print("No solution found")
        return None, list(explored), 0

    def backtracking_search(self, timeout=10.0):
        """Backtracking Search as CSP for 8-puzzle, starting from empty board."""
        start_time = time.time()

        def is_valid_state(state):
            """Kiểm tra trạng thái không có số trùng lặp."""
            used = set()
            for val in state:
                if val is not None and val in used:
                    return False
                if val is not None:
                    used.add(val)
            return True

        def is_complete(state):
            """Kiểm tra trạng thái đã đầy đủ (9 ô)."""
            return all(val is not None for val in state)

        def backtrack(state, path, used_values, pos):
            """Quay lui để điền số vào ô."""
            if time.time() - start_time > timeout:
                print("Timeout reached")
                return None, explored_states

            # Thêm trạng thái vào explored_states
            state_tuple = tuple(state)
            explored_states.add(state_tuple)
            path.append(state[:])

            # Nếu trạng thái đầy đủ, kiểm tra mục tiêu
            if is_complete(state):
                if self.is_solvable(state) and self.is_goal(state):
                    print(f"Solution found: {state}")
                    return path, explored_states
                return None, explored_states

            # Chọn ô tiếp theo để gán
            if pos >= 9:
                return None, explored_states

            # Thử gán các giá trị từ 0-8
            # Ưu tiên giá trị theo heuristic (gần với mục tiêu)
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            values = sorted(range(9), key=lambda x: abs(x - goal_state[pos]) if x not in used_values else float('inf'))
            for val in values:
                if val not in used_values:
                    # Gán giá trị
                    state[pos] = val
                    used_values.add(val)

                    # Kiểm tra ràng buộc
                    if is_valid_state(state):
                        # Tiếp tục với ô tiếp theo
                        result, sub_explored = backtrack(state, path, used_values, pos + 1)
                        explored_states.update(sub_explored)
                        if result:
                            return result, explored_states

                    # Quay lui: bỏ gán giá trị
                    state[pos] = None
                    used_values.remove(val)

            return None, explored_states

        # Khởi tạo trạng thái rỗng
        initial_state = [None] * 9  # Ma trận rỗng
        explored_states = set()
        path = []

        print(f"Starting backtracking with empty state: {initial_state}")
        solution, explored = backtrack(initial_state, path, set(), 0)

        if solution:
            print(f"Solution path length: {len(solution)}")
            return solution, list(explored)
        else:
            print("No solution found")
            return None, list(explored)

    def forward_checking_search(self, timeout=10.0):
        """Forward Checking Search as CSP for 8-puzzle, starting from empty board."""
        start_time = time.time()

        def is_valid_state(state):
            """Kiểm tra trạng thái không có số trùng lặp."""
            used = set()
            for val in state:
                if val is not None and val in used:
                    return False
                if val is not None:
                    used.add(val)
            return True

        def is_complete(state):
            """Kiểm tra trạng thái đã đầy đủ (9 ô)."""
            return all(val is not None for val in state)

        def update_domains(state, domains, pos, value):
            """Cập nhật miền giá trị sau khi gán giá trị."""
            new_domains = copy.deepcopy(domains)
            # Loại bỏ giá trị vừa gán khỏi miền của các ô chưa gán
            for i in range(9):
                if state[i] is None and value in new_domains[i]:
                    new_domains[i].remove(value)
            return new_domains

        def is_domains_valid(domains, state):
            """Kiểm tra xem miền của các ô chưa gán có hợp lệ (không rỗng)."""
            for i in range(9):
                if state[i] is None and not domains[i]:
                    return False
            return True

        def forward_check(state, path, domains, pos):
            """Quay lui với Forward Checking để điền số vào ô."""
            if time.time() - start_time > timeout:
                print("Timeout reached")
                return None, explored_states

            # Thêm trạng thái vào explored_states
            state_tuple = tuple(None if x is None else x for x in state)
            explored_states.add(state_tuple)
            path.append(copy.deepcopy(state))  # Sao chép sâu để tránh thay đổi

            # Nếu trạng thái đầy đủ, kiểm tra mục tiêu
            if is_complete(state):
                if self.is_solvable(state) and self.is_goal(state):
                    print(f"Solution found: {state}")
                    return path, explored_states
                return None, explored_states

            # Chọn ô tiếp theo để gán
            if pos >= 9:
                return None, explored_states

            # Thử gán các giá trị từ miền của ô hiện tại
            # Ưu tiên giá trị theo heuristic (gần với mục tiêu)
            goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            values = sorted(domains[pos], key=lambda x: abs(x - goal_state[pos]))
            for val in values:
                # Gán giá trị
                state[pos] = val
                # Cập nhật miền giá trị
                new_domains = update_domains(state, domains, pos, val)

                # Kiểm tra ràng buộc và miền
                if is_valid_state(state) and is_domains_valid(new_domains, state):
                    # Tiếp tục với ô tiếp theo
                    result, sub_explored = forward_check(state, path, new_domains, pos + 1)
                    explored_states.update(sub_explored)
                    if result:
                        return result, explored_states

                # Quay lui: bỏ gán giá trị
                state[pos] = None

            path.pop()  # Xóa trạng thái khỏi path khi quay lui
            return None, explored_states

        # Khởi tạo trạng thái rỗng và miền giá trị
        initial_state = [None] * 9
        initial_domains = {i: list(range(9)) for i in range(9)}
        explored_states = set()
        path = []

        print(f"Starting forward checking with empty state: {initial_state}")
        solution, explored = forward_check(initial_state, path, initial_domains, 0)

        if solution:
            print(f"Solution path length: {len(solution)}")
            return solution, list(explored)
        else:
            print("No solution found")
            return None, list(explored)

    def min_conflicts_search(self, timeout=10.0, max_steps=1000):
        """Min-Conflicts Search as CSP for 8-puzzle, using valid moves."""
        start_time = time.time()
        goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        explored_states = set()
        max_attempts = 50  # Tăng số lần thử để cải thiện khả năng tìm giải pháp

        def initialize_state():
            """Tạo trạng thái ngẫu nhiên khả giải."""
            state = goal_state[:]
            # Thực hiện các di chuyển ngẫu nhiên từ trạng thái mục tiêu
            for _ in range(100):  # Tạo trạng thái ngẫu nhiên bằng 100 di chuyển
                successors = self.get_successors(state)
                state = random.choice(successors)
            return state

        def count_conflicts(state):
            """Tính tổng khoảng cách Manhattan và số ô không khớp."""
            hamming = sum(1 for i in range(9) if state[i] != goal_state[i] and state[i] != 0)
            manhattan = self.heuristic(state)
            return manhattan + hamming  # Kết hợp để ưu tiên trạng thái tốt hơn

        def get_conflicted_vars(state):
            """Trả về danh sách các ô có xung đột (không khớp với goal_state)."""
            return [i for i in range(9) if state[i] != goal_state[i] and state[i] != 0]

        def get_min_conflict_move(state):
            """Tìm di chuyển của ô trống dẫn đến trạng thái có ít xung đột nhất."""
            zero_idx = state.index(0)
            successors = self.get_successors(state)
            if not successors:
                return None, float('inf')

            min_conflicts = float('inf')
            best_state = None
            for succ in successors:
                if self.is_solvable(succ):  # Chỉ xem xét trạng thái khả giải
                    conflicts = count_conflicts(succ)
                    if conflicts < min_conflicts:
                        min_conflicts = conflicts
                        best_state = succ
            return best_state, min_conflicts

        for attempt in range(max_attempts):
            if time.time() - start_time > timeout:
                print("Timeout reached")
                return None, list(explored_states)

            # Khởi tạo trạng thái ngẫu nhiên khả giải
            state = initialize_state()
            path = [state[:]]
            explored_states.add(tuple(state))
            print(f"Attempt {attempt + 1}: Initial state: {state}")

            # Lặp tối đa max_steps để giảm xung đột
            for step in range(max_steps):
                if time.time() - start_time > timeout:
                    print("Timeout reached")
                    return None, list(explored_states)

                # Kiểm tra nếu trạng thái là giải pháp
                if self.is_goal(state):
                    print(f"Solution found: {state}")
                    return path, list(explored_states)

                # Tìm di chuyển tốt nhất cho ô trống
                best_state, conflicts = get_min_conflict_move(state)
                if best_state is None:
                    break  # Không tìm thấy di chuyển khả thi, khởi động lại

                state = best_state[:]
                path.append(state[:])
                explored_states.add(tuple(state))
                print(f"Step {step + 1}: Updated state: {state}, conflicts: {conflicts}")

            print(f"Attempt {attempt + 1} failed, restarting")

        print("No solution found after max attempts")
        return None, list(explored_states)

    def q_learning_search(self, timeout=10.0):
        """Q-Learning Search."""
        start_time = time.time()
        Q = {}
        actions = [0, 1, 2, 3]  # 0: up, 1: down, 2: right, 3: left
        state = tuple(self.initial_state)
        path = [list(state)]
        explored_states = [list(state)]
        alpha = 0.2
        gamma = 0.9
        epsilon = 0.3
        max_episodes = 5000
        max_steps = 100
        convergence_threshold = 0.1

        for episode in range(max_episodes):
            if time.time() - start_time > timeout:
                return None, explored_states
            current_state = tuple(self.initial_state)
            max_delta = 0
            for step in range(max_steps):
                if current_state not in Q:
                    Q[current_state] = {a: 0 for a in actions}
                if random.random() < epsilon:
                    action = random.choice(actions)
                else:
                    action = max(Q[current_state], key=Q[current_state].get)
                idx = list(current_state).index(0)
                row, col = divmod(idx, 3)
                directions = {0: (-1, 0), 1: (1, 0), 2: (0, 1), 3: (0, -1)}
                dr, dc = directions[action]
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_idx = new_row * 3 + new_col
                    new_state = list(current_state)
                    new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                    new_state = tuple(new_state)
                    reward = -0.5 + (self.hamming_distance(current_state) - self.hamming_distance(new_state)) * 5
                    if self.is_goal(list(new_state)):
                        reward = 100
                else:
                    reward = -10
                    new_state = current_state
                if new_state not in Q:
                    Q[new_state] = {a: 0 for a in actions}
                old_value = Q[current_state][action]
                max_future_q = max(Q[new_state].values())
                Q[current_state][action] = old_value + alpha * (reward + gamma * max_future_q - old_value)
                max_delta = max(max_delta, abs(old_value - Q[current_state][action]))
                explored_states.append(list(new_state))
                current_state = new_state
                path.append(list(current_state))
                if self.is_goal(list(current_state)):
                    return path, explored_states
            epsilon = max(0.05, epsilon * 0.995)
            if max_delta < convergence_threshold:
                break
        current_state = tuple(self.initial_state)
        path = [list(current_state)]
        visited = {current_state}
        steps = 0
        while current_state != tuple(self.goal_state) and steps < max_steps:
            if current_state not in Q:
                break
            action = max(Q[current_state], key=Q[current_state].get)
            idx = list(current_state).index(0)
            row, col = divmod(idx, 3)
            directions = {0: (-1, 0), 1: (1, 0), 2: (0, 1), 3: (0, -1)}
            dr, dc = directions[action]
            new_row, new_col = row + dr, col + dc
            if not (0 <= new_row < 3 and 0 <= new_col < 3):
                break
            new_idx = new_row * 3 + new_col
            new_state = list(current_state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            new_state = tuple(new_state)
            if new_state in visited:
                break
            visited.add(new_state)
            path.append(list(new_state))
            explored_states.append(list(new_state))
            current_state = new_state
            steps += 1
        return path if self.is_goal(path[-1]) else None, explored_states