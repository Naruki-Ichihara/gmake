import gmaker as g
from svgpathtools import Path, Line, Arc
import numpy as np

printer = '/workdir/printers/composer.json'

# Printer setting
settings = {'extruderTemp': 260,
            'bedTemp': 60,
            'fanSpeed': 255,
            'retractionLiftZ': 0.8,
            'retractionSpeed': 0.0,
            'startExtraLength': 55, #45
            'startCompression': 0.05,
            'startCompressionTime': 2.5}

cut = 'M400\nM280 P0 S30\nG4 P100\nM280 P0 S90\nM400\n'
mergin = 44
asynchronousRate = 0.96
h = 0.125
R = 20
Rs = 220-R
Re = 50+R

paths = []
veritical = Path(Line((20+50j), (Rs+50j)))
arc = Path(Arc((220+Re*1j), (R+R*1j), np.deg2rad(90), False, False, (Rs+50j))).reversed()
horizontal = Path(Line((220+Re*1j), (220+150j)))
paths.append(veritical)
paths.append(arc)
paths.append(horizontal)

paths = g.paths2LinePaths(paths, division=20, sorting=False)

def ex(x, y):
    if x>150 and y<51:
        return 1.0*1.25
    elif 51<y<70:
        return 1.0
    else:
        return 1.0*asynchronousRate

feed = lambda x, y: 600

gpaths = [g.gPath(path) for path in paths]

layer = g.Layer(gpaths, ex, feed)
layer.cuttingConfig(cut, mergin)

model = g.Model(settings, printer, extrusion_symbol='U', oneStrokeMode=True)

model.stack(layer, 0.025)

model.generate('gcodes/TH0125T4_R20_CONT.gcode')