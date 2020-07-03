import time
from backtrack_solver import BacktrackSolver

start_time = time.time()
solver = BacktrackSolver(show_solving=False)
end_time = time.time()
print()
print(str(round(end_time - start_time, 3)) + "s taken to solve.")
input()
