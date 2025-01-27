# SQL
# prolog
import z3
chicken = z3.Int("chicken")
rabbits = z3.Int("rabbits")
solver = z3.Solver()
solver.add(chicken >= 1)
solver.add(rabbits >= 1)
solver.add(chicken + rabbits == 35)
solver.add(chicken * 2 + rabbits * 4 == 94)
if solver.check() == z3.sat:
    print(solver.model())
else:
    print("not satisfiable")


circle, triangle, square = z3.Ints("circle triangle square")
solver = z3.Solver()
solver.add(circle + circle == 10)
solver.add(circle * square + square == 12)
solver.add(circle * square - triangle * circle == circle)
if solver.check() == z3.sat:
    print(solver.model()[triangle])


A, B, C, D = z3.Bools("A B C D")
solver = z3.Solver()
solver.add(z3.Implies(A, B))
solver.add(z3.Implies(A, C))
solver.add(z3.Implies(B, D))
solver.add(z3.Implies(C, z3.Not(D)))
solver.add(A == True)
if solver.check() == z3.sat:
    print(solver.model())
else:
    print("not satisfiable")

