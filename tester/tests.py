def to_bin(n):
    return [int(i) for i in list(reversed(format(n, 'b')))]

def get_sorted_arrays(n, m):
    a = [i for i in range(1, n)]
    b = [i for i in range(1, m)]
    return a + [0] + b + [0]


main = {
    'basic/empty.imp': {
        'title': "No declarations, one command",
        'input': [[]],
        'output': [[1]]
    },
    'basic/read_put.imp': {
        'title': "Tests assignment, read and put",
        'input': [[10]],
        'output': [[10]]
    },
    'basic/assign.imp': {
        'title': "Tests assignment by :=",
        'input': [[]],
        'output': [[13]]
    },
    'basic/assign_ident.imp': {
        'title': "Tests assignment of a variable to another variable",
        'input': [[]],
        'output': [[5]]
    },
    'basic/add_multi.imp': {
        'title': "Multiple addition of identifiers and numbers",
        'input': [[]],
        'output': [[20]]
    },
    'basic/add_nums.imp': {
        'title': "Tests addition of two numbers",
        'input': [[]],
        'output': [[8]]
    },
    'basic/sum.imp': {
        'title': "Tests simple addition of two numbers",
        'input': [[]],
        'output': [[12]]
    },
    'basic/multi_subs.imp': {
        'title': "Tests all kinds of substraction",
        'input': [[]],
        'output': [[35]]
    },
    'basic/sum2.imp': {
        'title': "Another test for addition",
        'input': [
            [0, 5],
            [7, 101],
            [4, 20],
            [17, 8]
        ],
        'output': [
            [5, 10, 20, 12, 8],
            [108, 113, 20, 115, 8],
            [24, 29, 20, 31, 8],
            [25, 30, 20, 32, 8]
        ]
    },
    'basic/sub2.imp': {
        'title': "Broad test for substraction",
        'input': [
            [5, 0],
            [7, 101]
        ],
        'output': [
            [5, 0, 495, 0, 0, 2],
            [0, 94, 392, 0, 0, 2]
        ]
    },
    'basic/constants.imp': {
        'title': "Simple check for constants",
        'input': [
            []
        ],
        'output': [
            [0, 1, 2, 7, 13]
        ]
    },
    'basic/const_var_operations.imp': {
        'title': "Tests comments in most combinations",
        'input': [[]],
        'output': [[100] * 5 + [700] * 5 + [120000] * 5 + [100] * 5 + [1] * 5]
    },
    'basic/ugly_formatting.imp': {
        'title': "Ugly code formatting, test for flex",
        'input': [[]],
        'output': [[1, 2, 3]]
    },
    'comments/comments.imp': {
        'title': "Tests comments in most combinations",
        'input': [[]],
        'output': [[5]]
    },
    'conditions/simple_if.imp': {
        'title': "Tests all conditions in simple ifs",
        'input': [[1, 2, 3, 4]],
        'output': [[2, 3]]
    },
    'conditions/if_then_else.imp': {
        'title': "Tests simple if-then-else",
        'input': [
            [1, 2],
            [4, 3],
            [10, 10]
        ],
        'output': [
            [1], [3], [10]
        ]
    },
    'conditions/single_if.imp': {
        'title': "Single if just to test the jumps",
        'input': [
            [5, 15, 14], [10, 10, 11], [15, 5, 5]
        ],
        'output': [
            [5, 15, 15], [10], []
        ]
    },
    'conditions/all_conditions.imp': {
        'title': "Tests all kinds of condition in ifs",
        'input': [[1, 2, 3]],
        'output': [[2, 1, 2]]
    },
    'conditions/nested_if_else.imp': {
        'title': "Tests 3 nested if-then-else",
        'input': [
            [3, 1, 2, 4],
            [1, 2, 3, 4],
            [6, 5, 8, 8],
            [6, 5, 2, 1]
        ],
        'output': [
            [3, 4],
            [1],
            [8],
            [5]
        ]
    },
    'conditions/more_conditions.imp': {
        'title': "Another test for conditions",
        'input': [
            [10, 20],
            [21, 15],
            [2, 2],
            [2, 1]
        ],
        'output': [
            [11, 11, 20, 11, 10, 11, 33],
            [11, 21, 11, 11, 21, 11, 33],
            [11, 11, 2, 11, 11, 33],
            [11, 2, 11, 11, 11, 33]
        ]
    },
    'conditions/small_nested.imp': {
        'title': "Smaller test for nested (easier to debug)",
        'input': [
            [5, 6],
            [7, 7],
            [10, 6]
        ],
        'output': [
            [6], [7], []
        ]
    },
    'conditions/every_case_if.imp': {
        'title': 'Test for every condition',
        'input': [[]],
        'output': [[1, 4, 6, 2, 5, 6, 1, 3, 5]]
    },
    'loops/while.imp': {
        'title': "The most basic example of a while loop",
        'input': [[]],
        'output': [
            [5, 4, 3, 2, 1]
        ]
    },
    'loops/nested_while.imp': {
        'title': "Tests nested whiles",
        'input': [[]],
        'output': [
            [
                3, 3, 2, 3, 2, 1, 3, 3, 2,
                3, 2, 1, 3, 3, 2, 3, 2, 1,
            ]
        ]
    },
    'loops/nested_while2.imp': {
        'title': "Another test for nested whiles",
        'input': [
            [1, 2, 5]
        ],
        'output':
        [
            [4, 3, 2, 1]
        ]
    },
    'loops/while_multi.imp': {
        'title': "Tests while with multiplication",
        'input': [
            [2, 5],
            [3, 7],
            [4, 8]
        ],
        'output': [
            [2**i for i in range(6)],
            [3**i for i in range(8)],
            [4**i for i in range(9)]
        ]
    },
    'loops/for.imp': {
        'title': "Basic for loop with changing boundaries",
        'input': [[]],
        'output': [
            [5, 7, 9, 11, 13]
        ]
    },
    'loops/for_var.imp': {
        'title': "Another test for loops with variable range",
        'input': [
            [1, 5],
            [5, 1],
            [3, 3],
            [7, 8]
        ],
        'output': [
            [1, 2, 3, 4, 5],
            [],
            [3],
            [7, 8]
        ]
    },
    'loops/for_downto.imp': {
        'title': "Basic for loop downto",
        'input': [[]],
        'output': [
            list(reversed(range(1, 11)))
        ]
    },
    'loops/for_from_0.imp': {
        'title': "Tests FOR iterator starting at 0",
        'input': [[5], [0]],
        'output': [list(range(6)), [0]]
    },
    'loops/nested_fors.imp': {
        'title': "Tests three nested fors",
        'input': [[]],
        'output': [[837]]
    },
    'loops/nested_downtos.imp': {
        'title': "Tests three nested downto fors",
        'input': [[]],
        'output': [[837]]
    },
    'loops/without_iteration.imp': {
        'title': "Tests for loops without result",
        'input': [[]],
        'output': [[]]
    },
    'multi/num_num.imp': {
        'title': "Multiplication of two constants",
        'input': [[]],
        'output': [[15, 0, 36, 20]]
    },
    'multi/id_num.imp': {
        'title': "Multiplication of identifier and constant",
        'input': [[0], [1], [7], [10]],
        'output': [[0], [10], [70], [100]]
    },
    'divide/basic.imp': {
        'title': "Basic division of two constants",
        'input': [[]],
        'output': [[1, 3, 20, 0, 0, 0, 0 , 0]]
    },
    'divide/basic2.imp': {
        'title': "Basic division and mod",
        'input': [[]],
        'output': [[0, 107, 0, 108, 0, 109, 1, 0, 1, 1, 1, 2, 1, 3]]
    },
    'divide/modulo.imp': {
        'title': "The most basic modulo",
        'input': [
            [5, 1],
            [10, 33],
            [12, 5],
            [30, 0]
        ],
        'output': [
            [0], [10], [2], [0]
        ]
    },
    'arrays/basic.imp': {
        'title': "The most basic use of arrays",
        'input': [[]],
        'output': [[5, 7, 8]]
    },
    'arrays/sums.imp': {
        'title': "Tests sums of elements at variable positions",
        'input': [[10]],
        'output': [[24, 3, 4, 24, 10, 3, 4, 5, 6]]
    },
    'algorithms/prime_factors.imp': {
        'title': "Algorithm for finding prime factors of a number",
        'input': [
            [1024],
            [771],
            [123109],
            [0]
        ],
        'output': [
            [2, 10],
            [3, 1, 257, 1],
            [7, 1, 43, 1, 409, 1],
            [0, 1]
        ]
    },
    'algorithms/sieve.imp': {
        'title': 'Sieve of Eratosthenes',
        'input': [[]],
        'output': [
            [2, 3, 5, 7, 11, 13, 17, 19, 23,
             29, 31, 37, 41, 43, 47, 53, 59,
             61, 67, 71, 73, 79, 83, 89, 97]
        ]
    },
    'algorithms/binary.imp': {
        'title': "Algorithm for printing binary representation of a number",
        'input': [
            [5], [0], [33], [44], [1024]
        ],
        'output': [
            to_bin(5), [], to_bin(33), to_bin(44), to_bin(1024)
        ]
    },
    'algorithms/bubblesort.imp': {
        'title': "Bubble sort algorithm",
        'input': [
            []
        ],
        'output': [
            [3, 3, 5, 8, 15, 16, 19, 24, 40, 43]
        ]
    },
    'algorithms/palindrome.imp': {
        'title': '1 if input num is palindrom, 0 otherwise',
        'input': [
            [12321],
            [1010101],
            [111111],
            [10001],
            [100001],
            [123123123],
            [100101],
            [1111231111]
        ],
        'output': [[1], [1], [1], [1], [1], [0], [0], [0]]
    },
    'algorithms/merge.imp': {
        'title': "Algorithm for merging two sorted arrays",
        'input': [
            [1, 3, 5, 7, 9, 0, 2, 4, 6, 8, 0],
            get_sorted_arrays(10, 10),
            get_sorted_arrays(100, 100),
            get_sorted_arrays(2000, 5000)
        ],
        'output': [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            sorted(get_sorted_arrays(10, 10))[2:],
            sorted(get_sorted_arrays(100, 100))[2:],
            sorted(get_sorted_arrays(2000, 5000))[2:]
        ]
    },
    'old/numbers.imp': {
        'title': "Test for declaring reading and assigning variables",
        'input': [
            [13]
        ],
        'output': [
            [0, 1, 2, 10, 100, 10000, 1234567890, 28, 15, 999,
             555555555, 7777, 999, 11, 707, 7777]
        ]
    },
    'old/fib.imp': {
        'title': "Tests addition and array assignment performance",
        'input': [[1]],
        'output': [[121393]]
    },
    'old/factorial.imp': {
        'title': "Algorithm for measuring performance with factorial",
        'input': [[20]],
        'output': [[2432902008176640000]]
    },
    'old/fib_factorial.imp': {
        'title': "Another test for performance. Factorial + Fibonacci",
        'input': [[20]],
        'output': [[2432902008176640000, 17711]]
    },
    'old/tab.imp': {
        'title': "Tests arrays",
        'input': [[]],
        'output': [
            [0, 23, 44, 63, 80, 95, 108,
             119, 128, 135, 140, 143, 144,
             143, 140, 135, 128, 119, 108,
             95, 80, 63, 44, 23, 0]
        ]
    },
    'old/mod_mult.imp': {
        'title': "Algorithm of modular exponentiation",
        'input': [[1234567890, 1234567890987654321, 987654321]],
        'output': [[674106858]]
    },
    'old/loopiii.imp': {
        'title': "Another test for nested fors",
        'input': [
            [0, 0, 0],
            [1, 0, 2]
        ],
        'output': [
            [31000, 40900, 2222010],
            [31001, 40900, 2222012]
        ]
    },
    'old/for.imp': {
        'title': "Aaaand another test for fors",
        'input': [
            [12, 23, 34]
        ],
        'output': [
            [507, 4379, 0]
        ]
    },
    'old/sort.imp': {
        'title': "Sorting algorithm",
        'input': [[]],
        'output': [
            [5, 2, 10, 4, 20, 8, 17, 16, 11,
             9, 22, 18, 21, 13, 19, 3, 15, 6,
             7, 12, 14, 1, 1234567890, 1, 2, 3,
             4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
             15, 16, 17, 18, 19, 20, 21, 22]
        ]
    },
    'mix/ultras.imp': {
        'title': 'without any special reason',
        'input': [[]],
        'output':
        [[2, 37, 11, 12, 13, 13, 12, 11, 4096 ]]
    },
}
