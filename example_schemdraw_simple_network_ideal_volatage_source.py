from SchemdrawWrapper import Resistor, Line, Ground, SchemdrawNetwork, SchemdrawSolution, VoltageSource
from ClassicNodalAnalysis import nodal_analysis_solver
from schemdraw import Drawing
import schemdraw.elements as elm

if __name__ == '__main__':
    with Drawing() as d:
        d += VoltageSource(U=1, name='U1').up()
        d += Line().right()
        d += (R1:=Resistor(R=10, name='R1').down())
        d += Resistor(R=20, name='R2').at(R1.start).right()
        d += Resistor(R=30, name='R3').down()
        d += Line().left()
        d += Line().left()
        d += Ground()
        schemdraw_network = SchemdrawNetwork(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2')
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('R3')
        d += schemdraw_solution.draw_voltage('U1', reverse=True)