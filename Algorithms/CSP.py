class CSP:
    def __init__(self, variables, domains, constraints, assignments = None):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignment = assignments.copy() if assignments else {}

    #Verific daca valoarea atribuita nu afecteaza variabilele deja asignate
    def is_consistent(self, variable, value):
        for other_variable in self.assignment:
            if (variable, other_variable) in self.constraints:
                if not self.constraints[(variable, other_variable)](value, self.assignment[other_variable]):
                    return False
            if (other_variable, variable) in self.constraints:
                if not self.constraints[(other_variable, variable)](self.assignment[other_variable], value):
                    return False
        return True

    def get_MRV_unassigned_variable(self):
        unassigned_variables = [variable for variable in self.variables if variable not in self.assignment]
        return min(unassigned_variables, key=lambda x: len(self.domains[x]))

    #Elimminam valorile inconsistente din domeniile vecine
    def forward_checking(self, variable, value):
        constrained_domains = {var: list(self.domains[var]) for var in self.domains}

        for neighbor in self.variables:
            if neighbor == variable or neighbor in self.assignment:
                continue

            for val in self.domains[neighbor]:
                if (variable, neighbor) in self.constraints and not self.constraints[(variable, neighbor)](value, val):
                    constrained_domains[neighbor].remove(val)
                elif (neighbor, variable) in self.constraints and not self.constraints[(neighbor, variable)](val, value):
                    constrained_domains[neighbor].remove(val)

            if len(constrained_domains[neighbor]) == 0:
                return None

        return constrained_domains

    def ac3(self):
        queue = list(self.constraints.keys())

        domains = {}
        for variable in self.variables:
            if variable in self.assignment:
                domains[variable] = [self.assignment[variable]]
            else:
                domains[variable] = list(self.domains[variable])

        def revise(x, y):
            revised = False
            for vx in domains[x][:]:
                if all(not self.constraints[(x, y)](vx, vy) for vy in domains[y]):
                    domains[x].remove(vx)
                    revised = True
            return revised

        while queue:
            (x, y) = queue.pop(0)
            if (x, y) in self.constraints and revise(x, y):
                if not domains[x]:
                    return None

                for z in self.variables:
                    if z != x and (z, x) in self.constraints:
                        queue.append((z, x))
        return domains

    def backtracking(self, use_fc=False, use_mrv=False, use_ac3=False):
        if len(self.assignment) == len(self.variables):
            return self.assignment

        #Alegem variabila in functie de MRV sau alegem urmatoarea variabila disponibila neasignata
        if use_mrv:
            variable = self.get_MRV_unassigned_variable()
        else:
            variable = next(v for v in self.variables if v not in self.assignment)

        #Aleg domeniul simplu sau filtrat de AC3
        if use_ac3:
            ac3_domains = self.ac3()
            if ac3_domains is None:
                return None
            domain = ac3_domains[variable]
        else:
            domain = self.domains[variable]

        for value in domain:
            if not self.is_consistent(variable, value):
                continue

            self.assignment[variable] = value
            saved_domains = None

            if use_fc:
                saved_domains = self.domains
                fc_domains = self.forward_checking(variable, value)
                if fc_domains is None:
                    del self.assignment[variable]
                    continue

                self.domains = fc_domains

            result = self.backtracking(use_fc, use_mrv, use_ac3)
            if result is not None:
                return result

            del self.assignment[variable]
            if use_fc:
                self.domains = saved_domains

        return None
