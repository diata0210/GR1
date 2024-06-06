from ortools.linear_solver import pywraplp


def balanced_course_assignment_ilp(test_case):
    try:
        teachers = test_case['teachers']
        courses = test_case['courses']
        preferences = test_case['preferences']
        conflicts = test_case['conflicts']
        credits = test_case['credits']

        print("Teachers:", teachers)
        print("Courses:", courses)
        print("Preferences:", preferences)
        print("Conflicts:", conflicts)
        print("Credits:", credits)

        solver = pywraplp.Solver.CreateSolver('SCIP')

        if not solver:
            print('SCIP solver not available.')
            return

        # Decision variables
        X = {}
        for t in teachers:
            for c in courses:
                X[t, c] = solver.BoolVar(f'X_{t}_{c}')
        Y = [solver.IntVar(0, sum(credits), f'Y_{t}') for t in teachers]
        Z = solver.IntVar(0, sum(credits), 'Z')

        # Constraints
        # Each course must be assigned to exactly one teacher
        for c in courses:
            solver.Add(sum(X[t, c] for t in teachers) == 1)

        # Teachers can only be assigned courses from their preference list
        for t in teachers:
            for c in courses:
                if c not in preferences[t]:
                    solver.Add(X[t, c] == 0)

        # No two conflicting courses can be assigned to the same teacher
        for (i, j) in conflicts:
            for t in teachers:
                solver.Add(X[t, i] + X[t, j] <= 1)

        # Calculate the load for each teacher based on credits
        for t in teachers:
            solver.Add(Y[t] == sum(X[t, c] * credits[c] for c in courses))

        # The maximum load should be greater than or equal to the load of each teacher
        for t in teachers:
            solver.Add(Z >= Y[t])

        # Objective: Minimize the maximum load
        solver.Minimize(Z)

        # Solve the model
        print("Solving the model...")
        status = solver.Solve()

        # Output the results
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            print(f'Minimum possible maximum load: {Z.solution_value()}')
            for t in teachers:
                assigned_courses = [c for c in courses if X[t, c].solution_value() == 1]
                load = Y[t].solution_value()
                print(f'Teacher {t} is assigned courses {assigned_courses} with a load of {load}')
        else:
            print('No solution found.')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    test_cases = [
        {
            'teachers': [0, 1, 2],
            'courses': list(range(13)),
            'preferences': {
                0: [0, 2, 3, 4, 8, 10],
                1: [0, 1, 3, 5, 6, 7, 8],
                2: [1, 2, 3, 7, 9, 11, 12]
            },
            'conflicts': [(0, 2), (0, 4), (0, 8), (1, 4), (1, 10), (3, 7), (3, 9), (5, 11), (5, 12), (6, 8), (6, 12)],
            'credits': [3, 3, 4, 3, 4, 3, 3, 3, 4, 3, 3, 4, 4]
        },
        {
            'teachers': [0, 1],
            'courses': [0, 1, 2],
            'preferences': {0: [0, 1, 2], 1: [0, 1, 2]},
            'conflicts': [],
            'credits': [3, 3, 3]
        },
        {
            'teachers': [0, 1, 2],
            'courses': [0, 1, 2, 3, 4, 5],
            'preferences': {0: [0, 1, 3], 1: [2, 4, 5], 2: [1, 3, 5]},
            'conflicts': [(0, 2), (1, 3), (4, 5)],
            'credits': [3, 3, 2, 4, 2, 3]
        },
        {
            'teachers': [0, 1],
            'courses': [0, 1, 2, 3, 4],
            'preferences': {0: [0, 1, 3], 1: [2, 4]},
            'conflicts': [(1, 2), (3, 4)],
            'credits': [2, 2, 3, 4, 3]
        },
        {
            'teachers': [0, 1, 2, 3],
            'courses': [0, 1, 2, 3, 4, 5],
            'preferences': {0: [0, 1], 1: [2, 3], 2: [4, 5], 3: [0, 2, 4]},
            'conflicts': [(0, 1), (2, 3), (4, 5)],
            'credits': [3, 3, 3, 3, 3, 3]
        },
        {
            'teachers': [0, 1, 2, 3, 4, 5],
            'courses': list(range(20)),
            'preferences': {
                0: [0, 1, 2, 3, 4],
                1: [5, 6, 7, 8, 9],
                2: [10, 11, 12, 13, 14],
                3: [15, 16, 17, 18, 19],
                4: [0, 5, 10, 15],
                5: [1, 6, 11, 16]
            },
            'conflicts': [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19)],
            'credits': [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12]
        }
    ]

    for i, test_case in enumerate(test_cases):
        print(f"Test Case {i + 1}")
        balanced_course_assignment_ilp(test_case)
        print("\n" + "=" * 50 + "\n")
