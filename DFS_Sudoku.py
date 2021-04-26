import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial) # Define el tipo de tablero, ya sea 6x6 o 9x9
        self.height = int(self.type/3) # Define la altura del cuadrante (2 para 6x6, 3 para 9x9)

    def goal_test(self, state):
        # Suma esperada de cada fila, columna o cuadrante.
        total = sum(range(1, self.type+1))

        # Verifique filas y columnas y devuelva falso si el total no es válido
        for row in range(self.type):
            if (len(state[row]) != self.type) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(self.type):
                column_total += state[column][row]

            if (column_total != total):
                return False

        # Verifique los cuadrantes y devuelva falso si el total no es válido
        for column in range(0,self.type,3):
            for row in range(0,self.type,self.height):

                block_total = 0
                for block_row in range(0,self.height):
                    for block_column in range(0,3):
                        block_total += state[row + block_row][column + block_column]

                if (block_total != total):
                    return False

        return True

    # Devuelve un conjunto de números válidos de valores que no aparecen en usado
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Devuelve el primer lugar vacío en la cuadrícula (marcado con 0)
    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    # Filtrar valores válidos según la fila
    def filter_row(self, state, row):
        number_set = range(1, self.type+1) # Defines set of valid numbers that can be placed on board
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)
        return options

    # Filtrar valores válidos según la columna
    def filter_col(self, options, state, column):
        in_column = [] # List of valid values in spot's column
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)
        return options

    # Filtrar valores válidos según el cuadrante
    def filter_quad(self, options, state, row, column):
        in_block = [] # Lista de valores válidos en el cuadrante del spot
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)
        return options    

    def actions(self, state):
        row,column = self.get_spot(self.type, state) # Consigue el primer lugar vacío a bordo

        # Eliminar las opciones no válidas del lugar
        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_quad(options, state, row, column)

        # Ceder un estado para cada opción válida
        for number in options:
            new_state = copy.deepcopy(state)
            new_state[row][column] = number
            yield new_state

class Node:

    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        # Lista de devolución de estados válidos
        return [Node(state) for state in problem.actions(self.state)]

def DFS(problem):
    start = Node(problem.initial)
    if problem.goal_test(start.state):
        return start.state

    stack = []
    stack.append(start) # Coloque el nodo inicial en la pila

    while stack:
        node = stack.pop()
        if problem.goal_test(node.state):
            return node.state
        stack.extend(node.expand(problem)) # Agregue estados viables a la pila

    return None

def solve_dfs(board):
    print ("\nSolving with DFS...")
    start_time = time.time()
    problem = Problem(board)
    solution = DFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print ("Found solution")
        for row in solution:
            print (row)
    else:
        print ("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time))
