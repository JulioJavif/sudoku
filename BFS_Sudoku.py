from queue import Queue
import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial
        self.type = len(initial) # Define el tipo de tablero, ya sea 6x6 o 9x9
        self.height = int(self.type/3) # Define la altura del cuadrante (2 para 6x6, 3 para 9x9)

    # Devuelve un conjunto de números válidos de valores que no aparecen en usado
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Devuelve el primer lugar vacío en la cuadrícula (marcado con 0)
    def get_spot(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column   

    def actions(self, state):
        number_set = range(1, self.type+1) # Define un conjunto de números válidos que se pueden colocar a bordo
        in_column = [] # Lista de valores válidos en la columna del spot
        in_block = [] # Lista de valores válidos en el cuadrante del spot

        row,column = self.get_spot(self.type, state) # Consigue el primer lugar vacío a bordo

        # Filtrar valores válidos según la fila
        in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(number_set, in_row)

        # Filtrar valores válidos según la columna
        for column_index in range(self.type):
            if state[column_index][column] != 0:
                in_column.append(state[column_index][column])
        options = self.filter_values(options, in_column)

        # Filtrar con valores válidos según el cuadrante
        row_start = int(row/self.height)*self.height
        column_start = int(column/3)*3
        
        for block_row in range(0, self.height):
            for block_column in range(0,3):
                in_block.append(state[row_start + block_row][column_start + block_column])
        options = self.filter_values(options, in_block)

        for number in options:
            yield number, row, column      

    # Devuelve el tablero actualizado después de agregar un nuevo valor válido
    def result(self, state, action):

        play = action[0]
        row = action[1]
        column = action[2]

        # Agregar nuevo valor válido al tablero
        new_state = copy.deepcopy(state)
        new_state[row][column] = play

        return new_state

    # Use sumas de cada fila, columna y cuadrante para determinar la validez del estado de la placa
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

class Node:

    def __init__(self, state, action=None):
        self.state = state
        self.action = action

    # Usa cada acción para crear un nuevo estado de tablero
    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    # Devuelve el nodo con el nuevo estado de la placa
    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, action)

def BFS(problem):
    # Crear el nodo inicial del árbol de problemas con la placa original.
    node = Node(problem.initial)
    # Compruebe si la placa original es correcta y devuélvala inmediatamente si es válida
    if problem.goal_test(node.state):
        return node

    frontier = Queue()
    frontier.put(node)

    # Bucle hasta que se exploren todos los nodos o se encuentre una solución
    while (frontier.qsize() != 0):

        node = frontier.get()
        for child in node.expand(problem):
            if problem.goal_test(child.state):
                return child

            frontier.put(child)

    return None

def solve_bfs(board):
    print ("\nSolving with BFS...")
    start_time = time.time()

    problem = Problem(board)
    solution = BFS(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print ("Found solution")
        for row in solution.state:
            print (row)
    else:
        print ("No possible solutions")

    print ("Elapsed time: " + str(elapsed_time))
