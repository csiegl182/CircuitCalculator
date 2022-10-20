import schemdraw as sd
import CircuitCalculator.SchemdrawWrapper as sdw
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 10, 20, 10, 10
Uq1, Uq2, Uq3, Iq4 = 1, 1, 3, 0.1
R1, R2, R3, R4 = 10, 20, 30, 40
Uq1, Uq2, Uq3, Iq4 = 1, 2, 3, 0.1

with sd.Drawing() as d:
    d += sdw.LabelNode(id=5, id_loc='S')
    d += sdw.VoltageSource(V=Uq1, name='Uq1').up()
    d += sdw.Line().up()
    # d += sdw.Ground(theta=-90)
    d += sdw.LabelNode(id=0, id_loc='W')
    d += (_R1:=sdw.Resistor(R=R1, name='R1').right())
    d += sdw.LabelNode(id=1, id_loc='N')
    d += sdw.VoltageSource(V=Uq2, name='Uq2').down()
    d += sdw.LabelNode(id=2, id_loc='W')
    d += sdw.Resistor(R=R3, name='R3').down()
    d += (_R2:=sdw.Resistor(R=R2, name='R2').right().at(_R1.end))
    d += sdw.LabelNode(id=3, id_loc='N')
    d += sdw.VoltageSource(V=Uq3, name='Uq3').down()
    d += sdw.LabelNode(id=4, id_loc='W')
    d += sdw.Resistor(R=R4, name='R4').down()
    d += sdw.Line().right().at(_R2.end)
    d += sdw.Line().down()
    d += sdw.CurrentSource(I=Iq4, name='Iq4').down()
    d += sdw.Line().left()
    d += sdw.Line().left()
    d += sdw.Line().left()
    schemdraw_network = sdw.SchemdrawNetwork(d)
    schemdraw_solution = sdw.SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R1')
    d += schemdraw_solution.draw_voltage('R2')
    d += schemdraw_solution.draw_voltage('R3')
    d += schemdraw_solution.draw_voltage('R4')
    d += schemdraw_solution.draw_voltage('Uq1')
    d += schemdraw_solution.draw_current('R1')
    d += schemdraw_solution.draw_current('R2')
    d += schemdraw_solution.draw_current('R3')
    d += schemdraw_solution.draw_current('R4')
    d += schemdraw_solution.draw_current('Iq4')