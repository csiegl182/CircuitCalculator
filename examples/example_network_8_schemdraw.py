import schemdraw as sd
from CircuitCalculator.SimpleCircuit.Elements import VoltageSource, CurrentSource, Resistor, Line, LabelNode
from CircuitCalculator.SimpleCircuit.Network import SchemdrawNetwork, SchemdrawSolution
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4, R5 = 10, 20, 30, 40, 50
Uq1, Uq2, Uq3, Iq1 = 1, 2, 3, 0.1

with sd.Drawing(unit=5) as d:
    d += (N0 := LabelNode(id='0', id_loc='S'))
    d += VoltageSource(V=Uq1, name='Uq1', precision=1).up().length(2*d.unit)
    d += (N1 := LabelNode(id='1', id_loc='N'))
    d += Line().right()
    d += Line().up()
    d += VoltageSource(V=Uq2, name='Uq2', precision=1).right()
    d += Line().down()
    d += (N2 := LabelNode(id='2', id_loc='N'))
    d += Resistor(R=R2, name='R2').left()
    d += Resistor(R=R1, name='R1').down().length(2*d.unit)
    d += Resistor(R=R3, name='R3').right()
    d += CurrentSource(I=Iq1, name='Iq1', precision=1).up()
    d += Resistor(R=R4, name='R4').up()
    d += Line().right()
    d += Resistor(R=R5, name='R5').down().length(2*d.unit)
    d += Line().left()
    d += Line().at(N0.start).right()
    schemdraw_network = SchemdrawNetwork(d)
    schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
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