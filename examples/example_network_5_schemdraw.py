import schemdraw as sd
from CircuitCalculator.SimpleCircuit.Elements import VoltageSource, Resistor, Line, LabelNode, CurrentSource
from CircuitCalculator.SimpleCircuit.Network import SchemdrawNetwork, SchemdrawSolution
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 10, 20, 30, 40
Uq1, Uq2, Uq3, Iq4 = 1, 2, 3, 0.1

with sd.Drawing(unit=5) as d:
    d += LabelNode(id='5', id_loc='S')
    d += VoltageSource(V=Uq1, name='Uq1', precision=1).up()
    d += Line().up()
    d += LabelNode(id='0', id_loc='W')
    d += (_R1:=Resistor(R=R1, name='R1').right())
    d += LabelNode(id='1', id_loc='N')
    d += VoltageSource(V=Uq2, name='Uq2', precision=1).down()
    d += LabelNode(id='2', id_loc='W')
    d += Resistor(R=R3, name='R3').down()
    d += (_R2:=Resistor(R=R2, name='R2').right().at(_R1.end))
    d += LabelNode(id='3', id_loc='N')
    d += VoltageSource(V=Uq3, name='Uq3', precision=1).down()
    d += LabelNode(id='4', id_loc='W')
    d += Resistor(R=R4, name='R4').down()
    d += Line().right().at(_R2.end)
    d += Line().down()
    d += CurrentSource(I=Iq4, name='Iq4').down()
    d += Line().left()
    d += Line().left()
    d += Line().left()
    schemdraw_network = SchemdrawNetwork(d)
    schemdraw_solution = SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R1')
    d += schemdraw_solution.draw_voltage('R2')
    d += schemdraw_solution.draw_voltage('R3')
    d += schemdraw_solution.draw_voltage('R4')
    d += schemdraw_solution.draw_current('R1', ofst=1.2)
    d += schemdraw_solution.draw_current('R2', ofst=1.2)
    d += schemdraw_solution.draw_current('R3', ofst=1.2)
    d += schemdraw_solution.draw_current('R4', ofst=1.2)