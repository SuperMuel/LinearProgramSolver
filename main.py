from scipy.optimize import linprog


class PL:
    MAX = "MAX"
    MIN = "MIN"
    def __init__(self):
        self.mode = PL.MAX
        self.vars = self.ask_Z()
        self.n = len(self.vars)
        self.A_ineq = self.ask_A()
        self.m = len(self.A_ineq)
        self.B_ineq = self.ask_B()




    def ask_Z(self):
        def print_vars(vars):
            print(f"{self.mode} Z = ", end="")
            for i, value in enumerate(vars, start=1):
                print(f"{'+' if i!=1 else ''} {value}*x{i} ",end="")

        print(f'Please enter the coeffs of the economic function. {self.mode} Z = ... \n enter \'d\' to remove previous value')
        k = "_"
        vars = []
        while not vars or k != "":
            k = input()
            if k == "d" and vars:
                vars.pop()
            else:
                try:
                    k = float(k)
                    vars.append(k)
                except Exception:
                    pass
            print_vars(vars)
        return vars

    class MatrixNotFull(Exception):
        pass
    def ask_A(self):
        def print_matrix(A):
            print("[",end="")
            for l in A :
                print(f" {l}")
            print("]")
        print("Enter A ineq matrix. Enter d to erase. Enter f to finish.")
        k = "_"
        A =[]
        while True:
            print_matrix(A)
            k = input()
            try:
                if k == "":
                    k = 0
                k = float(k)
            except Exception:
                if k == "f":
                    if not A or len(A[-1]) != self.n:
                        continue
                    else:
                        return A
                if k == "d":
                    try:
                        if not A[-1]:
                            A.pop()
                        else:
                            (A[-1]).pop()
                        continue
                    except Exception as err:
                        print(err)
                        continue
            if A == [] or len(A[-1])==self.n:
                A.append([k])
            else:
                A[-1].append(k)

    def ask_B(self):
        def print_B(B):
            print("[")
            for b in B:
                print(b)
            print("]")
        print(f"Enter the {self.m} right members of inequations")
        B = []
        while len(B) < self.m:
            print_B(B)
            k = input()
            try:
                k = float(k)
            except Exception:
                if k == "d" and B:
                    B.pop()
                    continue
            B.append(k)
        print_B(B)
        return B

    def solve_PL(self):
        def max_to_min(Z_max):
            return [-x for x in Z_max]
        if self.mode == PL.MAX:
            Z = max_to_min(self.vars)
        else:
            Z = self.vars


        return linprog(c=Z, A_ub=self.A_ineq, b_ub=self.B_ineq, method="simplex")["x"]

Pl = PL()
print(Pl.solve_PL())