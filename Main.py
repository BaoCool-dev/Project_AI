from Algorithm import algorithm
from UI import UI
import matplotlib.pyplot as plt
import os
import platform
import time

class Main:
    def __init__(self):
        #self.initial_state = [1, 2, 3, 4, 0, 6, 7, 5, 8]
        self.initial_state = [0, 1, 3, 4, 2, 5, 7, 8, 6]
        self.algorithm = algorithm(self.initial_state)
        self.ui = UI(self)
        self.performance_history = {
            "BFS": [], "DFS": [], "UCS": [], "IDS": [], "A*": [], "IDA*": [],
            "Greedy": [], "Simple HC": [], "Steepest HC": [], "Random HC": [],
            "Simulated Annealing": [], "Beam Search": [], "Genetic": [],
            "And-Or Tree": [], "Belief": [], "POS": [], "Backtrack": [],
            "Forward": [], "MinConf": [], "QLearn": []
        }

    def set_initial_state(self, state):
        if isinstance(state, tuple):
            state = self.algorithm.tuple_to_list_state(state)
        self.initial_state = state
        inversions = 0
        state_without_zero = [x for x in state if x != 0]
        for i in range(len(state_without_zero)):
            for j in range(i + 1, len(state_without_zero)):
                if state_without_zero[i] > state_without_zero[j]:
                    inversions += 1
        zero_idx = state.index(0)
        zero_row, zero_col = divmod(zero_idx, 3)
        goal_zero_row, goal_zero_col = 2, 2
        taxicab_distance = abs(zero_row - goal_zero_row) + abs(zero_col - goal_zero_col)
        is_solvable = (inversions + taxicab_distance) % 2 == 0
        self.algorithm.initial_state = state
        return is_solvable

    def run_algorithm(self, algorithm_name, initial_belief=None):
        algorithm_map = {
            "BFS": self.algorithm.bfs,
            "DFS": lambda: self.algorithm.dfs(timeout=30.0, max_depth=20),
            "UCS": self.algorithm.ucs,
            "IDS": self.algorithm.ids,
            "A*": self.algorithm.a_star,
            "IDA*": self.algorithm.ida_star,
            "Greedy": self.algorithm.greedy_search,
            "Simple HC": self.algorithm.simple_hill_climbing,
            "Steepest HC": self.algorithm.steepest_ascent_hill_climbing,
            "Random HC": self.algorithm.random_hill_climbing,
            "Simulated Annealing": self.algorithm.simulated_annealing,
            "Beam Search": self.algorithm.beam_search,
            "Genetic": self.algorithm.genetic_algorithm,
            "And-Or Tree": self.algorithm.and_or_search,
            "Belief": lambda: self.algorithm.belief_state_search(initial_belief),
            "POS": lambda: self.algorithm.partial_observable_search(initial_belief),
            "Backtrack": self.algorithm.backtracking_search,
            "Forward": self.algorithm.forward_checking_search,
            "MinConf": self.algorithm.min_conflicts_search,
            "QLearn": self.algorithm.q_learning_search,
        }
        if algorithm_name in algorithm_map:
            try:
                start_time = time.time()
                result = algorithm_map[algorithm_name]()
                elapsed_time = (time.time() - start_time) * 1000
                if algorithm_name in ["Belief", "POS"]:
                    if isinstance(result, tuple) and len(result) == 3:
                        solution, explored_states, total_steps = result
                        steps = total_steps
                        path_length = total_steps
                        if not isinstance(solution, list):
                            print(f"Error: Solution is not a list: {solution}")
                            solution = []
                        converted_solution = []
                        for belief_set in solution:
                            if not isinstance(belief_set, (list, tuple, set)):
                                print(f"Error: Invalid belief_set in solution: {belief_set}")
                                continue
                            belief_set_converted = []
                            for state in belief_set:
                                if not isinstance(state, (list, tuple)):
                                    print(f"Error: Invalid state in belief_set: {state}")
                                    continue
                                state_converted = self.algorithm.tuple_to_list_state(state) if isinstance(state, tuple) else state
                                belief_set_converted.append(state_converted)
                            converted_solution.append(belief_set_converted)
                        solution = converted_solution
                    else:
                        solution = result
                        explored_states = []
                        steps = 0
                        path_length = 0
                else:
                    if isinstance(result, tuple) and len(result) == 2:
                        solution, explored_states = result
                        if algorithm_name in ["Backtrack", "Forward"] and solution:
                            steps = sum(1 for state in solution[-1] if state is not None) - 1
                            path_length = len(solution)
                        else:
                            steps = len(solution) - 1 if solution else 0
                            path_length = len(solution) if solution else 0
                    else:
                        solution = result
                        explored_states = []
                        steps = 0
                        path_length = 0
                self.performance_history[algorithm_name].append({
                    "runtime": elapsed_time,
                    "steps": steps,
                    "states_explored": len(explored_states),
                    "path_length": path_length
                })
                if algorithm_name in ["Belief", "POS"]:
                    return solution, total_steps
                return solution
            except Exception as e:
                print(f"Error running {algorithm_name}: {str(e)}")
                raise
        else:
            raise ValueError(f"Algorithm '{algorithm_name}' is not valid.")

    def display_algorithm_info(self):
        with open("algorithm_info.txt", "w") as file:
            file.write("=== Algorithm Performance Info ===\n\n")
            for algo, runs in self.performance_history.items():
                if not runs:
                    continue
                file.write(f"Algorithm: {algo}\n")
                for i, run in enumerate(runs, 1):
                    file.write(f"  Run {i}:\n")
                    file.write(f"    Steps: {run['steps']}\n")
                    file.write(f"    States Explored: {run['states_explored']}\n")
                    file.write(f"    Runtime: {run['runtime']:.2f} ms\n")
                    file.write(f"    Path Length: {run['path_length']}\n")
                file.write("\n")
            file.write("================================\n")
        try:
            if platform.system() == "Windows":
                os.startfile("algorithm_info.txt")
            elif platform.system() == "Darwin":
                os.system("open algorithm_info.txt")
            else:
                os.system("xdg-open algorithm_info.txt")
        except Exception as e:
            print(f"Error opening file: {e}")

    def plot_performance(self):
        algorithms = []
        avg_states_explored = []
        avg_runtimes = []

        for algo, runs in self.performance_history.items():
            if runs:
                algorithms.append(algo)
                states = [run["states_explored"] for run in runs]
                avg_states_explored.append(sum(states) / len(states))
                runtimes = [run["runtime"] for run in runs]
                avg_runtimes.append(sum(runtimes) / len(runtimes))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle("Performance Comparison", fontsize=16)

        ax1.bar(algorithms, avg_states_explored, color="lightblue")
        ax1.set_ylabel("States Explored")
        for i, v in enumerate(avg_states_explored):
            ax1.text(i, v + max(avg_states_explored) * 0.01, f"{v:.0f}", ha="center", fontweight="bold")

        ax2.bar(algorithms, avg_runtimes, color="lightcoral")
        ax2.set_ylabel("Time (ms)")
        for i, v in enumerate(avg_runtimes):
            ax2.text(i, v + max(avg_runtimes) * 0.01, f"{v:.2f}", ha="center", fontweight="bold")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    app = Main()
    app.run()