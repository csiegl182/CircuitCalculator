from CircuitCalculator.SchemdrawWrapper import VoltageSource, Resistor, Line, Ground, SchemdrawNetwork, SchemdrawSolution
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver
from schemdraw import Drawing

if __name__ == '__main__':
    with Drawing() as d:
        d += (U1:=VoltageSource(V=1, R=0, name='U1').up())
        d += Line().right()
        d += (R1:=Resistor(R=10, name='R1').down())
        d += Line().left()
        d += Ground()
        d += Resistor(R=20, name='R2').at(R1.start).right()
        d += Resistor(R=30, name='R3').down()
        d += Line().left()
        schemdraw_network = SchemdrawNetwork(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2')
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('R3')
        d += schemdraw_solution.draw_current('R3', start=False)
        d += schemdraw_solution.draw_current('U1')