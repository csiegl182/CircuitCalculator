import schemdraw as sd
import CircuitCalculator.SchemdrawWrapper as sdw
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
Uq1, Uq2, Uq3, Iq1 = 1, 2, 3, 0.1

with sd.Drawing(unit=5) as d:
    d += (N0 := sdw.LabelNode(id=0, id_loc='S'))
    d += sdw.VoltageSource(V=Uq1, name='Uq1', precision=1).up().length(2*d.unit)
    d += (N1 := sdw.LabelNode(id=1, id_loc='N'))
    d += sdw.Line().right()
    d += sdw.Line().up()
    d += sdw.VoltageSource(V=Uq2, name='Uq2', precision=1).right()
    d += sdw.Line().down()
    d += (N2 := sdw.LabelNode(id=2, id_loc='N'))
    d += sdw.Resistor(R=R2, name='R2').left()
    d += sdw.Resistor(R=R1, name='R1').down().length(2*d.unit)
    d += sdw.Resistor(R=R3, name='R3').right()
    d += sdw.CurrentSource(I=Iq1, name='Iq1', precision=1).up()
    d += sdw.Resistor(R=R4, name='R4').up()
    d += sdw.Line().right()
    d += sdw.Resistor(R=R5, name='R5').down().length(2*d.unit)
    d += sdw.Line().left()
    d += sdw.Line().at(N0.start).right()
    schemdraw_network = sdw.SchemdrawNetwork(d)
    schemdraw_solution = sdw.SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R1', precision=5)
    d += schemdraw_solution.draw_voltage('R2', precision=5)
    d += schemdraw_solution.draw_voltage('R3', precision=5)
    d += schemdraw_solution.draw_voltage('R4', precision=5)
    d += schemdraw_solution.draw_voltage('R5', precision=5)
    d += schemdraw_solution.draw_voltage('Iq1', precision=5)
    d += schemdraw_solution.draw_current('R1', ofst=1.2)
    d += schemdraw_solution.draw_current('R2', ofst=1.2)
    d += schemdraw_solution.draw_current('R3', ofst=1.2)
    d += schemdraw_solution.draw_current('R4', ofst=1.2)
    d += schemdraw_solution.draw_current('R5', ofst=1.2)
    d += schemdraw_solution.draw_current('Uq1', ofst=1.2)
    d += schemdraw_solution.draw_current('Uq2', ofst=1.2)