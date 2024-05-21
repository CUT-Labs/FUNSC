import schemdraw
from schemdraw import logic
import matplotlib.pyplot as plt
import matplotlib.backends.backend_svg

matplotlib.use('TkAgg')
# from schemdraw.parsing import logicparse

# with logicparse('(a and b) and (y nand x)', outlabel='$f(x)$') as d:
#    d.save('my_circuit.svg')

# with schemdraw.Drawing() as d:
#      d += (a := logic.And().label('b', 'in1'))
#      d += (b := logic.Or().at(a.out, dy=-.5).anchor('in1').label('f', 'out'))
#      d += logic.Line().at(a.out).to(b.in1)
#      d += logic.Line().at(a.in2).toy(b.in2)
#      d += logic.Line().at(b.in2).tox(a.in2.x-.5).label('a', 'left')

# logic gate drawing of (x^2)/10 + x/15 + 4/5
schemdraw.use('matplotlib')

with schemdraw.Drawing(file="assets/my_circuit.png") as d:
    d += (g1 := logic.Nand().right().label('0.75', 'in1').label('X', 'in2'))
    d += g1.label('G1', 'center')
    d += (g2 := logic.Nand().at(g1.out).right().anchor('in2').label('0.6667', 'in1', ofst=(0, 0.5)))
    d += g2.label('G2', 'center')
    d += (g3 := logic.Nand().at(g2.out).right().anchor('in1'))
    d += g3.label('G3', 'center')
    d += (g4 := logic.Nand().at(g3.out).right().anchor('in2').label('0.2', 'in1', ofst=(0, 0.5)).label('$f(x)$', 'out'))
    d += g4.label('G4', 'center')
    d += logic.Wire('n', k=-0.5).at(g1.out).to(g3.in2)

d.draw()

for elem in d.elements:
    if type(elem) is schemdraw.logic.logic.And or type(elem) is schemdraw.logic.logic.Nand:
        print('-' * 15)
        print(elem)
        print(elem.segments)
        print(elem.__str__())