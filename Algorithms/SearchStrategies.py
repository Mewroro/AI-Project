import heapq
import random
import time
from collections import deque
import concurrent.futures

class SearchStrategies:
    def __init__(self):
        self.times = {}
        self.solutions = {}

    def bfs(self, problem):
        frontier = deque([problem.initial_state()])
        visited = set()

        while frontier:
            state = frontier.popleft()

            if problem.is_goal(state):
                return state

            visited.add(state)

            for next_state in problem.successors(state):
                if next_state not in visited:
                    frontier.append(next_state)
        return None
    
    def backtracking(self, problem, state=None):
        if state is None:
            state = problem.initial_state()

        if problem.is_goal(state):
            return state

        for next_state in problem.successors(state):
            result = self.backtracking(problem, next_state)
            if result is not None:
                return result
        return None

    def iterative_deepening(self, problem, max_depth=50):
        def dls(state, depth):
            if problem.is_goal(state):
                return state
            if depth == 0:
                return None
            for next_state in problem.successors(state):
                result = dls(next_state, depth - 1)
                if result is not None:
                    return result
            return None

        for depth in range(1, max_depth + 1):
            result = dls(problem.initial_state(), depth)
            if result is not None:
                return result
        return None

    def uniform_cost(self, problem):
        start = problem.initial_state()
        frontier = []
        heapq.heappush(frontier, (0, start))
        cost_so_far = {start: 0}
        while frontier:
            cost, state = heapq.heappop(frontier)
            if problem.is_goal(state):
                return state
            for next_state in problem.successors(state):
                new_cost = cost_so_far[state] + problem.cost(state, next_state)
                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, next_state))
        return None

    def greedy_best_first(self, problem):
        start = problem.initial_state()
        frontier = []
        counter = 0

        heapq.heappush(frontier, (problem.heuristic(start), counter, start))

        use_visited = not (hasattr(problem, "type") and problem.type == "coloring")
        visited = set() if use_visited else None

        while frontier:
            _, _, state = heapq.heappop(frontier)

            if problem.is_goal(state):
                return state

            if use_visited:
                visited.add(state)

            for next_state in problem.successors(state):
                if use_visited and next_state in visited:
                    continue

                counter += 1
                heapq.heappush(
                    frontier,
                    (problem.heuristic(next_state), counter, next_state)
                )

        return None

    def simulated_annealing(self, problem, T=1000, alpha=0.95):
        current = problem.initial_state()
        while T > 1:
            neighbors = problem.successors(current)
            if not neighbors:
                return current
            next_state = random.choice(neighbors)
            delta = problem.heuristic(next_state) - problem.heuristic(current)
            if delta < 0 or random.random() < pow(2.71828, -delta / T):
                current = next_state
            T *= alpha
        return current

    def beam_search(self, problem, k=3):
        beam = [problem.initial_state()]
        while beam:
            new_beam = []
            for state in beam:
                new_beam.extend(problem.successors(state))
            if not new_beam:
                return beam[0]
            beam = sorted(new_beam, key=lambda s: problem.heuristic(s))[:k]
            for state in beam:
                if problem.is_goal(state):
                    return state
        return beam[0] if beam else None

    def hill_climbing(self, problem):
        current = problem.initial_state()

        while True:
            neighbors = problem.successors(current)
            if not neighbors:
                return current

            next_state = min(neighbors, key=lambda s: problem.heuristic(s))

            if problem.heuristic(next_state) >= problem.heuristic(current):
                return current

            current = next_state

    def knight_mrv(self, problem):
        path = list(problem.initial_state())
        n = problem.n

        def remaining_moves(state, move):
            x, y = move
            cnt = 0
            for dx, dy in problem.moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in state:
                    cnt += 1
            return cnt

        while len(path) < n * n:
            x, y = path[-1]
            moves = [(x + dx, y + dy) for dx, dy in problem.moves
                     if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in path]
            if not moves:
                return None

            path.append(min(moves, key=lambda m: remaining_moves(path, m)))
        return tuple(path)
    
    def astar(self, problem):
        start = problem.initial_state()
        frontier = []
        heapq.heappush(frontier, (0, start))
        cost_so_far = {start: 0}

        while frontier:
            _, state = heapq.heappop(frontier)

            if problem.is_goal(state):
                return state

            for next_state in problem.successors(state):
                new_cost = cost_so_far[state] + problem.cost(state, next_state)

                if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                    cost_so_far[next_state] = new_cost
                    priority = new_cost + problem.heuristic(next_state)
                    heapq.heappush(frontier, (priority, next_state))
        return None

    def run_with_timeout(self, func, problem, timeout=5.0):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(func, problem)
            try:
                result = future.result(timeout=timeout)
                return result
            except concurrent.futures.TimeoutError:
                return None

    def run(self, name, func, problem, timeout=5.0):
        start = time.perf_counter()
        solution = self.run_with_timeout(func, problem, timeout)
        end = time.perf_counter()
        if solution is None:
            self.times[name] = float('inf')
            self.solutions[name] = None
        else:
            self.times[name] = end - start
            self.solutions[name] = solution

    def run_all(self, problem):
        self.times.clear()
        self.solutions.clear()
        strategies = []

        if not hasattr(problem, "type"):
            return

        if problem.type == "nqueens":
            strategies = [
                ("Backtracking", self.backtracking),
                ("HillClimbing", self.hill_climbing),
                ("Simulated Annealing", self.simulated_annealing),
            ]

        elif problem.type == "coloring":
            strategies = [
                ("Backtracking", self.backtracking),
                ("HillClimbing", self.hill_climbing),
                ("Greedy", self.greedy_best_first),
            ]

        elif problem.type == "hanoi":
            strategies = [
                ("BFS", self.bfs),
                ("A*", self.astar),
            ]

        elif problem.type == "knight":
            strategies = [
                ("Simulated Annealing", self.simulated_annealing),
                ("MRV", self.knight_mrv),
            ]

        if not strategies:
            return

        for name, func in strategies:
            self.run(name, func, problem, timeout=2.0)

    def best_strategy(self):
        valid_times = {k: v for k, v in self.times.items() if v != float('inf')}
        if not valid_times:
            return None, None

        name = min(valid_times, key=valid_times.get)
        return name, valid_times[name]

    def print_results(self):
            for name, t in self.times.items():
                print(f"{name}: {t:.6f} sec")
            print(f"\n Cea mai rapida strategie: {self.best_strategy()}")
