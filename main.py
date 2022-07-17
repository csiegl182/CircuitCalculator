import json
from SchemdrawWrapper import RealCurrentSource, Resistor, Line, Ground, SchemdrawNetwork, draw_voltage, draw_current
from schemdraw import Drawing

if __name__ == '__main__':
    with Drawing() as d:
        d += RealCurrentSource(I=1, R=100, name='I1').up()
        d += (R1:=Resistor(R=10, name='R1').right())
        d += Resistor(R=20, name='R2').down()
        d += Line().left()
        d += Ground()
        schemdraw_network = SchemdrawNetwork(d)
        d += draw_voltage(schemdraw_network, 'R1')
        # d += draw_current(schemdraw_network, 'R1')
        d += draw_voltage(schemdraw_network, 'R2', reverse=False)
        # d += draw_current(schemdraw_network, 'R2')
        # d += draw_voltage(schemdraw_network, 'I1', reverse=True)

print(json.dumps(schemdraw_network.dependency_list, indent=2))