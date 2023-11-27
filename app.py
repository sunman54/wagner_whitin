import tkinter as tk
from tkinter import ttk
from collections import namedtuple

# Define a namedtuple for the constants
Constants = namedtuple("Constants", ["order_cost", "holding_cost"])

# Function to run the Wagner-Whitin algorithm
def wagner_whitin(demands, constants):
    order_cost = constants.order_cost
    holding_cost = constants.holding_cost

    d_cumsum = CumSumList(demands)
    assert demands[-1] > 0, "Final demand should be positive"

    T = len(demands)
    F = {-1: 0}
    t_star_star = 0
    cover_by = {}

    for t in range(len(demands)):
        if demands[t] == 0:
            F[t] = F[t - 1]
            cover_by[t] = t
            continue

        assert demands[t] > 0

        S_t = 0
        min_args = []

        for j in reversed(range(t_star_star, t + 1)):
            S_t += holding_cost * d_cumsum.sum_between(j + 1, t)
            min_args.append(order_cost + S_t + F[j - 1])

        argmin = min_args.index(min(min_args))
        t_star_star = max(t_star_star, t - argmin)
        F[t] = min_args[argmin]
        cover_by[t] = t - argmin

    t = T - 1
    solution = [0] * T

    while True:
        j = cover_by[t]
        solution[j] = sum(demands[j: t + 1])
        t = j - 1
        if j == 0:
            break

    return {"cost": F[len(demands) - 1], "solution": solution}

class CumSumList:
    def __init__(self, elements):
        self.cumsums = [0] * len(elements)
        partial_sum = 0
        for i, element in enumerate(elements):
            partial_sum += element
            self.cumsums[i] = partial_sum

    def sum_between(self, i, j):
        if i > j:
            return 0
        top = self.cumsums[j] if j < len(self.cumsums) else self.cumsums[-1]
        low = self.cumsums[i - 1] if i >= 1 else 0
        return top - low

class WagnerWhitinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wagner-Whitin Solver")

        # Input variables
        self.demands_var = tk.StringVar()
        self.order_cost_var = tk.IntVar(value=300)
        self.holding_cost_var = tk.IntVar(value=1)

        # Output variables
        self.optimal_cost_var = tk.StringVar()
        self.optimal_solution_var = tk.StringVar()

        # Create input frames
        self.create_input_frame()

        # Create output frames
        self.create_output_frame()

        # Create solve button
        self.create_solve_button()

    def create_input_frame(self):
        input_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        input_frame.grid(column=0, row=0, padx=10, pady=10)

        ttk.Label(input_frame, text="Demands (comma-separated):").grid(column=0, row=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.demands_var).grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(input_frame, text="Order Cost:").grid(column=0, row=1, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.order_cost_var).grid(column=1, row=1, padx=10, pady=5)

        ttk.Label(input_frame, text="Holding Cost:").grid(column=0, row=2, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.holding_cost_var).grid(column=1, row=2, padx=10, pady=5)

    def create_output_frame(self):
        output_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10))
        output_frame.grid(column=0, row=1, padx=10, pady=10)

        ttk.Label(output_frame, text="Optimal Cost:").grid(column=0, row=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.optimal_cost_var).grid(column=1, row=0, padx=10, pady=5)

        ttk.Label(output_frame, text="Optimal Solution (Order Quantities):").grid(column=0, row=1, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.optimal_solution_var).grid(column=1, row=1, padx=10, pady=5)

    def create_solve_button(self):
        solve_button = ttk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(column=0, row=2, pady=10)

    def solve(self):
        try:
            demands = list(map(int, self.demands_var.get().split(',')))
            order_cost = self.order_cost_var.get()
            holding_cost = self.holding_cost_var.get()

            constants = Constants(order_cost, holding_cost)

            # Run the Wagner-Whitin algorithm
            result = wagner_whitin(demands, constants)

            # Display the result
            self.optimal_cost_var.set(result["cost"])
            self.optimal_solution_var.set(result["solution"])
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter valid integers separated by commas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WagnerWhitinApp(root)
    root.mainloop()
