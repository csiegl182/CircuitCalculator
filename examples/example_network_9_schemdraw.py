import schemdraw as sd
import CircuitCalculator.SchemdrawWrapper as sdw
from CircuitCalculator.AdvancedNodalAnalysis import nodal_analysis_solver

R1, R2, R3, R4 = 15, 5, 20, 20
Uq = 120
Iq = 4

with sd.Drawing(unit=5) as d:
    d += sdw.CurrentSource(I=Iq, name='Iq').up()
    d += sdw.Line().right()
    d += (R2_ := sdw.Resistor(R=R2, name='R2').right())
    d += (R3_ := sdw.Resistor(R=R3, name='R3').down())
    d += sdw.Line().left()
    d += sdw.Line().left()
    d += sdw.Line().right().at(R3_.end)
    d += sdw.Resistor(R=R4, name='R4').up()
    d += sdw.VoltageSource(V=Uq, name='Uq', precision=1, reverse=True).left()
    d += sdw.Resistor(R=R1, name='R1').down().at(R2_.start)
    schemdraw_network = sdw.SchemdrawNetwork(d)
    schemdraw_solution = sdw.SchemdrawSolution(schemdraw_network, nodal_analysis_solver)
    d += schemdraw_solution.draw_voltage('R4', precision=3, reverse=True)