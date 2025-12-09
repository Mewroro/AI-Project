class Nash:
    def __init__(self, matrix, player1_strategies, player2_strategies):
        self.row_count = len(matrix)
        self.column_count = len(matrix[0])

        self.player1_strategies = player1_strategies
        self.player2_strategies = player2_strategies

        self.equilibrium_count = 0
        self.equilibria = []

        #player 1 va contine liste cu valorile de pe coloane
        self.payoffs_player1 = []

        #player 2 va contine liste cu valorile de pe linii
        self.payoffs_player2 = []

        for row in range(self.row_count):
            row_player2 = []
            for column in range(self.column_count):

                if len(self.payoffs_player1) < column + 1:
                    self.payoffs_player1.append([])

                row_player2.append(matrix[row][column][1])
                self.payoffs_player1[column].append(matrix[row][column][0])

            self.payoffs_player2.append(row_player2)

        self.best_strategy_matrix = [[0 for _ in range(self.column_count)] for _ in range(self.row_count)]

    def find_pure_nash(self):
        #marcam valorile maxime pentru player 1
        for column in range(self.column_count):
            row_payoffs = self.payoffs_player1[column]
            max_payoff = max(row_payoffs)

            for row in range(self.row_count):
                if row_payoffs[row] == max_payoff:
                    self.best_strategy_matrix[row][column] += 1

        # marcam valorile maxime pentru player 2
        for row in range(self.row_count):
            column_payoffs = self.payoffs_player2[row]
            max_payoff = max(column_payoffs)

            for column in range(self.column_count):
                if column_payoffs[column] == max_payoff:
                    self.best_strategy_matrix[row][column] += 2

        for row in range(self.row_count):
            for column in range(self.column_count):
                if self.best_strategy_matrix[row][column] == 3:
                    player1_strategy = self.player1_strategies[row]
                    player2_strategy = self.player2_strategies[column]

                    self.equilibria.append((player1_strategy, player2_strategy))
                    self.equilibrium_count += 1

    def get_player1_dominant_strategies(self):
        dominant_strategies = []
        for row in range(self.row_count):
            is_dominant = True
            for column in range(self.column_count):
                if self.best_strategy_matrix[row][column] not in (1, 3):
                    is_dominant = False
                    continue

            if is_dominant:
                dominant_strategies.append(self.player1_strategies[row])
        return dominant_strategies

    def get_player2_dominant_strategies(self):
        dominant_strategies = []
        for column in range(self.column_count):
            is_dominant = True
            for row in range(self.row_count):
                if self.best_strategy_matrix[row][column] not in (2, 3):
                    is_dominant = False
                    continue

            if is_dominant:
                dominant_strategies.append(self.player2_strategies[column])
        return dominant_strategies
