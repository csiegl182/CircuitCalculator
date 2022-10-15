from SchemdrawWrapper import RealCurrentSource, Resistor, Line, Ground, SchemdrawNetwork, SchemdrawSolution
from ClassicNodalAnalysis import nodal_analysis_solver
from schemdraw import Drawing

if __name__ == '__main__':
    with Drawing() as d:
        d += RealCurrentSource(I=1, R=100, name='I1').up()
        d += (R1:=Resistor(R=10, name='R1').right())
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
        schemdraw_network = SchemdrawNetwork(d)
        schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
        d += schemdraw_solution.draw_voltage('R1')
        d += schemdraw_solution.draw_current('R1')
        d += schemdraw_solution.draw_voltage('R2', reverse=False)
        d += schemdraw_solution.draw_current('R2')
        d += schemdraw_solution.draw_voltage('I1')