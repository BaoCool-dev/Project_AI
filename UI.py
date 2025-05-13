import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import random
import time


class UI:
    def __init__(self, algorithm_handler):
        self.root = tk.Tk()
        self.root.title("8-Puzzle Solver")
        self.root.attributes('-fullscreen', True)
        self.algorithm_handler = algorithm_handler
        self.root.configure(bg="#f0f0f0")
        #self.puzzle_numbers = [1, 2, 3, 4, 0, 6, 7, 5, 8]
        self.puzzle_numbers =  [0, 1, 3, 4, 2, 5, 7, 8, 6]
        self.cells = []
        self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.after_ids = []

        self._load_background_image()
        self.setup_ui()
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))

    def cancel_animation(self):
        for after_id in self.after_ids:
            self.root.after_cancel(after_id)
        self.after_ids.clear()

    def _load_background_image(self):
        image_path = "image\\bg.jpg"
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Background image {image_path} not found")
            image = Image.open(image_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            image = image.resize((screen_width, screen_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.background_label = tk.Label(self.root, image=self.photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError as e:
            messagebox.showwarning("Warning", str(e))
            self.root.configure(bg="#f0f0f0")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {str(e)}")
            self.root.configure(bg="#f0f0f0")

    def setup_ui(self):
        title = tk.Label(self.root, text="8-Puzzle Solver", font=("Comic Sans MS", 20, "bold"),
                         bg="#FFFFFF", fg="#FF0000")
        title.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#FFFFFF")
        main_frame.pack(pady=5, padx=10)
        self._setup_puzzle_boards(main_frame)
        self._setup_algorithm_buttons()

    def _setup_puzzle_boards(self, main_frame):
        puzzle_frame = tk.Frame(main_frame, bg="#F8BBD0", bd=2, relief=tk.SUNKEN)
        puzzle_frame.grid(row=0, column=0, padx=10, pady=5)

        self.cells = [tk.Label(puzzle_frame,text="" if self.puzzle_numbers[i] == 0 else str(self.puzzle_numbers[i]),
                               width=5, height=2, font=("Comic Sans MS", 18, "bold"), bg="#E1BEE7",
                               fg="#E83D30", relief=tk.RAISED, borderwidth=2)
                      for i in range(9)]
        for i, cell in enumerate(self.cells):
            cell.grid(row=i // 3, column=i % 3, padx=2, pady=2)

        goal_frame = tk.Frame(main_frame, bg="#F8BBD0", bd=2, relief=tk.SUNKEN)
        goal_frame.grid(row=0, column=1, padx=20, pady=10)

        goal_cells = [tk.Label(goal_frame, text="" if self.goal_state[i] == 0 else str(self.goal_state[i]),
                               width=5, height=2, font=("Comic Sans MS", 18, "bold"), bg="#E1BEE7",
                               fg="#E83D30", relief=tk.RAISED, borderwidth=2)
                      for i in range(9)]
        for i, cell in enumerate(goal_cells):
            cell.grid(row=i // 3, column=i % 3, padx=2, pady=2)

        tk.Label(main_frame, text="Initial State", font=("Comic Sans MS", 14, "bold"),
                 bg="#FFFFFF", fg="#00FF00").grid(row=1, column=0)
        tk.Label(main_frame, text="Goal State", font=("Comic Sans MS", 14, "bold"),
                 bg="#FFFFFF", fg="#00FF00").grid(row=1, column=1)

    def _setup_algorithm_buttons(self):
        button_frame = tk.Frame(self.root, bg="#F8BBD0")
        button_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Comic Sans MS", 10), padding=5)

        button_layout = [
            ["BFS", "DFS", "UCS", "IDS"],
            ["A*", "IDA*", "Greedy", "Beam Search"],
            ["Simple HC", "Steepest HC", "Random HC", "Simulated Annealing"],
            ["Genetic", "And-Or Tree", "Belief", "POS"],
            ["Backtrack", "Forward", "MinConf", "QLearn"],
            ["View", "Info", "Restart", "Exit"]
        ]

        for row_idx, row in enumerate(button_layout):
            for col_idx, algo in enumerate(row):
                if algo == "Exit":
                    ttk.Button(button_frame, text=algo, command=self.exit_app).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "Restart":
                    ttk.Button(button_frame, text=algo, command=self.on_restart).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "View":
                    ttk.Button(button_frame, text=algo, command=self.algorithm_handler.plot_performance).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "Info":
                    ttk.Button(button_frame, text=algo, command=self.algorithm_handler.display_algorithm_info).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo in ["Belief", "POS"]:
                    ttk.Button(button_frame, text=algo, command=lambda a=algo: self.show_belief_interface(a)).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "Backtrack":
                    ttk.Button(button_frame, text=algo, command=lambda a=algo: self.solve_backtrack(a)).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "Forward":
                    ttk.Button(button_frame, text=algo, command=lambda a=algo: self.solve_forward(a)).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                elif algo == "MinConf":
                    ttk.Button(button_frame, text=algo, command=lambda a=algo: self.solve_minconf(a)).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
                else:
                    ttk.Button(button_frame, text=algo, command=lambda a=algo: self.solve(a)).grid(
                        row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")

    def update_puzzle_board(self, state):
        if isinstance(state, tuple):
            state = [num for row in state for num in row]
        self.puzzle_numbers = state
        for i, cell in enumerate(self.cells):
            cell.config(text=str(self.puzzle_numbers[i]) if self.puzzle_numbers[i] is not None else "-")
            cell.config(text="" if self.puzzle_numbers[i] == 0 else str(self.puzzle_numbers[i]))
            
    def animate_solution(self, solution, belief_cells=None):
        self.cancel_animation()
        self.after_ids = []

        if belief_cells:
            for i, belief_set in enumerate(solution):
                def update_belief(k=i):
                    if not belief_cells[0][0].winfo_exists():
                        return
                    for j in range(min(3, len(belief_set))):
                        state = belief_set[j]
                        if isinstance(state, tuple):
                            state = [num for row in state for num in row]
                        for k, cell in enumerate(belief_cells[j]):
                            if cell.winfo_exists():
                                cell.config(text="" if state[k] == 0 else str(state[k]))

                after_id = self.root.after(i * 500, update_belief)
                self.after_ids.append(after_id)
        else:
            for i, state in enumerate(solution):
                if isinstance(state, tuple):
                    state = [num for row in state for num in row]
                after_id = self.root.after(i * 500,lambda s=state: self.update_puzzle_board(s))
                self.after_ids.append(after_id)

        if belief_cells:
            belief_window = belief_cells[0][0].master.master
            if isinstance(belief_window, tk.Toplevel):
                belief_window.protocol("WM_DELETE_WINDOW", lambda: [self.cancel_animation(), belief_window.destroy()])

    def on_restart(self):
        self.cancel_animation()
        #self.puzzle_numbers = [1, 2, 3, 4, 0, 6, 7, 5, 8]
        self.puzzle_numbers =  [0, 1, 3, 4, 2, 5, 7, 8, 6]
        self.update_puzzle_board(self.puzzle_numbers)

    def solve_backtrack(self, algorithm):
        messagebox.showinfo("Backtrack CSP",
                            "Backtracking will start from an empty board and fill numbers to reach the goal state.")
        self.update_puzzle_board([None] * 9)
        try:
            start_time = time.time()
            result = self.algorithm_handler.run_algorithm(algorithm)
            elapsed_time = (time.time() - start_time) * 1000
            if isinstance(result, tuple):
                solution, explored_states = result
            else:
                solution = result
                explored_states = []

            if solution and isinstance(solution, list) and len(solution) > 0:
                print(f"{algorithm} solution path (length: {len(solution)}):")
                for step in solution:
                    print(step)
                messagebox.showinfo("Result",
                                    f"Solved with {algorithm} in {elapsed_time:.2f} ms, {len(solution)} steps.")
                self.animate_solution(solution)
            else:
                print(f"No solution found with {algorithm}")
                messagebox.showwarning("Result", f"No solution found with {algorithm} in {elapsed_time:.2f} ms.")
                self.on_restart()
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run {algorithm}: {str(e)}")
            self.on_restart()

    def solve_forward(self, algorithm):
        messagebox.showinfo("Forward Checking CSP",
                            "Forward Checking will start from an empty board and fill numbers to reach the goal state.")
        self.update_puzzle_board([None] * 9)
        try:
            start_time = time.time()
            result = self.algorithm_handler.run_algorithm(algorithm)
            elapsed_time = (time.time() - start_time) * 1000
            if isinstance(result, tuple):
                solution, explored_states = result
            else:
                solution = result
                explored_states = []

            if solution and isinstance(solution, list) and len(solution) > 0:
                print(f"{algorithm} solution path (length: {len(solution)}):")
                for step in solution:
                    print(step)
                messagebox.showinfo("Result",
                                    f"Solved with {algorithm} in {elapsed_time:.2f} ms, {len(solution)} steps.")
                self.animate_solution(solution)
            else:
                print(f"No solution found with {algorithm}")
                messagebox.showwarning("Result", f"No solution found with {algorithm} in {elapsed_time:.2f} ms.")
                self.on_restart()
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run {algorithm}: {str(e)}")
            self.on_restart()

    def solve_minconf(self, algorithm):
        messagebox.showinfo("Min-Conflicts CSP",
                            "Min-Conflicts will start from an empty board, randomly assign numbers, and adjust to reach the goal state.")
        self.update_puzzle_board([None] * 9)
        try:
            start_time = time.time()
            result = self.algorithm_handler.run_algorithm(algorithm)
            elapsed_time = (time.time() - start_time) * 1000
            if isinstance(result, tuple):
                solution, explored_states = result
            else:
                solution = result
                explored_states = []

            if solution and isinstance(solution, list) and len(solution) > 0:
                print(f"{algorithm} solution path (length: {len(solution)}):")
                for step in solution:
                    print(step)
                messagebox.showinfo("Result",
                                    f"Solved with {algorithm} in {elapsed_time:.2f} ms, {len(solution)} steps.")
                self.animate_solution(solution)
            else:
                print(f"No solution found with {algorithm}")
                messagebox.showwarning("Result", f"No solution found with {algorithm} in {elapsed_time:.2f} ms.")
                self.on_restart()
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run {algorithm}: {str(e)}")
            self.on_restart()

    def solve(self, algorithm):
        is_solvable = self.algorithm_handler.set_initial_state(self.puzzle_numbers)
        if not is_solvable:
            messagebox.showerror("Error", "The initial state is not solvable!")
            return
        try:
            start_time = time.time()
            result = self.algorithm_handler.run_algorithm(algorithm)
            elapsed_time = (time.time() - start_time) * 1000
            if isinstance(result, tuple):
                solution, explored_states = result
            else:
                solution = result
                explored_states = []

            if solution and isinstance(solution, list) and len(solution) > 0:
                print(f"{algorithm} solution path (length: {len(solution)}):")
                for step in solution:
                    print(step)
                messagebox.showinfo("Result",
                                    f"Solved with {algorithm} in {elapsed_time:.2f} ms, {len(solution)} steps.")
                self.animate_solution(solution)
            else:
                print(f"No solution found with {algorithm}")
                messagebox.showwarning("Result", f"No solution found with {algorithm} in {elapsed_time:.2f} ms.")
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run {algorithm}: {str(e)}")

    def show_belief_interface(self, algorithm):
        initial_belief = [
            [1, 2, 3, 4, 5, 6, 7, 0, 8],
            [1, 2, 3, 4, 0, 6, 7, 5, 8],
            [1, 2, 3, 4, 5, 6, 0, 7, 8]
        ]
        if algorithm == "Belief":
            initial_belief = self.algorithm_handler.algorithm.bfs_for_belief(self.puzzle_numbers)
        else:  # POS
            initial_belief = self.algorithm_handler.algorithm.find_states_with_one_at_00(self.puzzle_numbers)

        if not isinstance(initial_belief, (list, tuple)) or not initial_belief or len(initial_belief) != 3:
            messagebox.showerror("Error", f"Failed to initialize valid belief states for {algorithm}.",
                                parent=self.root)
            return

        initial_belief = [
            self.algorithm_handler.algorithm.list_to_tuple_state(state) if isinstance(state, list) else state for state
            in initial_belief]

        belief_window = tk.Toplevel(self.root)
        belief_window.title(f"{algorithm} State Search")
        belief_window.attributes('-fullscreen', True)
        belief_window.configure(bg="#f0f0f0")
        belief_window.initial_belief = initial_belief

        image_path = "image\\bg.jpg"
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Background image {image_path} not found")
            image = Image.open(image_path)
            image = image.resize((belief_window.winfo_screenwidth(), belief_window.winfo_screenheight()), Image.LANCZOS)
            belief_window.photo = ImageTk.PhotoImage(image)
            bg_label = tk.Label(belief_window, image=belief_window.photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError as e:
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {str(e)}")

        tk.Label(belief_window, text=f"{algorithm} State Search", font=("Comic Sans MS", 30, "bold"),
                bg="#FFFFFF", fg="#424242").pack(pady=10)

        # Khung chính: màu hồng
        main_frame = tk.Frame(belief_window, bg="#F8BBD0")
        main_frame.pack(pady=10, padx=20)

        belief_frames = []
        belief_cells = []
        for i in range(3):
            # Khung belief: màu hồng
            frame = tk.Frame(main_frame, bg="#F8BBD0", bd=2, relief=tk.SUNKEN)
            frame.grid(row=0, column=i, padx=5, pady=5)
            state = self.algorithm_handler.algorithm.tuple_to_list_state(initial_belief[i])
            # Các ô: màu tím nhạt
            cells = [tk.Label(frame, text="" if state[j] == 0 else str(state[j]),
                            width=4, height=2, font=("Comic Sans MS", 14, "bold"), bg="#E1BEE7",
                            fg="#424242", relief=tk.RAISED, borderwidth=2)
                    for j in range(9)]
            for j, cell in enumerate(cells):
                cell.grid(row=j // 3, column=j % 3, padx=1, pady=1)
            belief_frames.append(frame)
            belief_cells.append(cells)
            tk.Label(main_frame, text=f"Belief {i + 1}", font=("Comic Sans MS", 10, "bold"),
                    bg="#F8BBD0", fg="#424242").grid(row=1, column=i)

        # Khung mục tiêu: màu hồng
        goal_frame = tk.Frame(main_frame, bg="#F8BBD0", bd=2, relief=tk.SUNKEN)
        goal_frame.grid(row=0, column=3, padx=20, pady=10)
        # Các ô mục tiêu: màu tím nhạt
        goal_cells = [tk.Label(goal_frame, text="" if self.goal_state[i] == 0 else str(self.goal_state[i]),
                            width=4, height=2, font=("Comic Sans MS", 14, "bold"), bg="#E1BEE7",
                            fg="#424242", relief=tk.RAISED, borderwidth=2)
                    for i in range(9)]
        for i, cell in enumerate(goal_cells):
            cell.grid(row=i // 3, column=i % 3, padx=1, pady=1)
        tk.Label(main_frame, text="Goal State", font=("Comic Sans MS", 12, "bold"),
                bg="#F8BBD0", fg="#424242").grid(row=1, column=3)

        info_frame = tk.Frame(belief_window, bg="#f0f0f0")
        info_frame.pack(pady=10)
        time_label = tk.Label(info_frame, text="Running Time: 0.00 ms", font=("Comic Sans MS", 12),
                            bg="#f0f0f0", fg="#424242")
        time_label.pack()
        steps_label = tk.Label(info_frame, text="Steps: 0", font=("Comic Sans MS", 12),
                            bg="#f0f0f0", fg="#424242")
        steps_label.pack()

        button_frame = tk.Frame(belief_window, bg="#f0f0f0")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Run", command=lambda: self.run_belief_algorithm(
            algorithm, belief_window.initial_belief, belief_cells, time_label, steps_label)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Back", command=lambda: [self.cancel_animation(), belief_window.destroy()]).pack(
            side=tk.LEFT, padx=5)

        belief_window.protocol("WM_DELETE_WINDOW", lambda: [self.cancel_animation(), belief_window.destroy()])

    def run_belief_algorithm(self, algorithm, initial_belief, belief_cells, time_label, steps_label):
        try:
            if not isinstance(initial_belief, (list, tuple, set)) or not initial_belief or len(initial_belief) != 3:
                messagebox.showerror("Error", "Invalid belief states. Please edit belief states and try again.",
                                     parent=belief_cells[0][0].master)
                return

            print(f"Initial Belief States for {algorithm}:")
            for i, state in enumerate(initial_belief):
                state_list = self.algorithm_handler.algorithm.tuple_to_list_state(state) if isinstance(state,
                                                                                                       tuple) else state
                print(f"Belief {i + 1}: {state_list}")

            start_time = time.time()
            result = self.algorithm_handler.run_algorithm(algorithm, initial_belief=initial_belief)
            elapsed_time = (time.time() - start_time) * 1000
            if isinstance(result, tuple) and len(result) == 3:
                solution, explored_states, total_steps = result
            elif isinstance(result, tuple) and len(result) == 2:
                solution, explored_states = result
                total_steps = len(solution) - 1 if solution else 0
            else:
                solution = result
                explored_states = []
                total_steps = 0

            if solution and isinstance(solution, list) and len(solution) > 0:
                print(f"{algorithm} solution path (length: {len(solution)}):")
                step_list = []
                for belief_set in solution:
                    if not isinstance(belief_set, (list, tuple, set)):
                        print(f"Error: Invalid belief_set in solution: {belief_set}")
                        continue
                    belief_set_converted = []
                    for state in belief_set:
                        if not isinstance(state, (list, tuple)):
                            print(f"Error: Invalid state in belief_set: {state}")
                            continue
                        state_converted = self.algorithm_handler.algorithm.tuple_to_list_state(state) if isinstance(
                            state, tuple) else state
                        belief_set_converted.append(state_converted)
                    step_list.append(belief_set_converted)
                print(step_list)

                time_label.config(text=f"Running Time: {elapsed_time:.2f} ms")
                steps_label.config(text=f"Steps: {total_steps}")
                messagebox.showinfo("Result", f"Solved with {algorithm} in {elapsed_time:.2f} ms, {total_steps} steps.",
                                    parent=belief_cells[0][0].master)
                self.animate_solution(solution, belief_cells)
            else:
                print(f"No solution found with {algorithm}")
                time_label.config(text=f"Running Time: {elapsed_time:.2f} ms")
                steps_label.config(text="Steps: 0")
                messagebox.showwarning("Result", f"No solution found with {algorithm} in {elapsed_time:.2f} ms.",
                                       parent=belief_cells[0][0].master)
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
            messagebox.showerror("Error", f"Failed to run {algorithm}: {str(e)}",
                                 parent=belief_cells[0][0].master)

    def exit_app(self):
        self.cancel_animation()
        self.root.destroy()

    def run(self):
        self.root.mainloop()