# Balanced Course Assignment
This project aims to solve the problem of assigning courses to teachers in a way that balances the workload among teachers as evenly as possible. 
The solution uses Google's OR-Tools library for both Constraint Programming (CP-SAT) and Integer Linear Programming (ILP).

## Requirements
- Python 3.6+
- OR-Tools

You can install OR-Tools using pip:
```sh
pip install ortools
```

## How to Run

1. Clone the repository or download the scripts.
2. Ensure you have the required dependencies installed.
3. Run the script using Python:

```sh
python balanced_course_assignment.py
```

or

```sh
python balanced_course_assignment_ilp.py
```

## Input Format

The input is a list of test cases. Each test case is a dictionary with the following keys:

- `teachers`: A list of teacher IDs.
- `courses`: A list of course IDs.
- `preferences`: A dictionary where keys are teacher IDs and values are lists of preferred course IDs.
- `conflicts`: A list of tuples, each containing two course IDs that conflict with each other.
- `credits`: A list of integers representing the credit hours for each course.

Example:

```python
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
    }
]
```

## Output

The script will print the following information for each test case:

- The minimum possible maximum load.
- The assignment of courses to each teacher along with their respective loads.

Example output:

```
Test Case 1
Teachers: [0, 1, 2]
Courses: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Preferences: {0: [0, 2, 3, 4, 8, 10], 1: [0, 1, 3, 5, 6, 7, 8], 2: [1, 2, 3, 7, 9, 11, 12]}
Conflicts: [(0, 2), (0, 4), (0, 8), (1, 4), (1, 10), (3, 7), (3, 9), (5, 11), (5, 12), (6, 8), (6, 12)]
Credits: [3, 3, 4, 3, 4, 3, 3, 3, 4, 3, 3, 4, 4]
Solving the model...
Minimum possible maximum load: 10
Teacher 0 is assigned courses [0, 3, 10] with a load of 10
Teacher 1 is assigned courses [1, 5, 6, 7] with a load of 10
Teacher 2 is assigned courses [2, 4, 8, 9, 11, 12] with a load of 10
```

## Error Handling

If an error occurs during the execution, it will be caught and printed to the console.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Google OR-Tools](https://developers.google.com/optimization) for providing the optimization library used in this project.
