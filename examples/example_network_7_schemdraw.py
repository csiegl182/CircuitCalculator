import schemdraw as sd
import CircuitCalculator.SchemdrawWrapper as sdw
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 10, 20, 30, 40
Uq1, Uq2, Uq3, Iq4 = 1, 2, 3, 0.1

with sd.Drawing(unit=5) as d:
    d += sdw.VoltageSource(V=Uq1, name='Uq1', precision=1).up()
    d += sdw.LabelNode(id='1', id_loc='W')
    d += sdw.VoltageSource(V=Uq2, name='Uq2', precision=1).up()
    d += (_R1:=sdw.Resistor(R=R1, name='R1').right())
    d += sdw.Line().down()
    d += sdw.Line().down()
    d += sdw.Line().left()
    schemdraw_network = sdw.SchemdrawNetwork(d)
    schemdraw_solution = sdw.SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R1')
    d += schemdraw_solution.draw_current('R1', ofst=1.2)