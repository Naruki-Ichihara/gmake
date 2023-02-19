import gmaker as g
from svgpathtools import Path, Line

printer = '/workdir/printers/composer.json'

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
asynchronousRate = 1.00
h = 0.125

paths = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        paths.append(Path(Line((70+50j)+(0+shift*1j), (220+50j)+(0+shift*1j))))
    else:
        paths.append(Path(Line((220+50j)+(0+shift*1j), (70+50j)+(0+shift*1j))))

paths = g.paths2LinePaths(paths, division=100, sorting=False)

anchor_paths_r = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        anchor_paths_r.append(Path(Line((70+40j)+(shift*1+0j), (70+73j)+(shift*1+0j))))
    else:
        anchor_paths_r.append(Path(Line((70+73j)+(shift*1+0j), (70+40j)+(shift*1+0j))))
anchor_paths_r = g.paths2LinePaths(anchor_paths_r, division=100, sorting=False)
        
anchor_paths_l = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        anchor_paths_l.append(Path(Line((220+73j)-(shift*1+0j), (220+40j)-(shift*1+0j))))
    else:
        anchor_paths_l.append(Path(Line((220+40j)-(shift*1+0j), (220+73j)-(shift*1+0j))))
anchor_paths_l = g.paths2LinePaths(anchor_paths_l, division=100, sorting=False)


ex = lambda x, y: 1.0*asynchronousRate
feed = lambda x, y: 600

gpaths = [g.gPath(path) for path in paths]
gpaths_r = [g.gPath(path) for path in anchor_paths_r]
gpaths_l = [g.gPath(path) for path in anchor_paths_l]

layer = g.Layer(gpaths, ex, feed)
layer_r = g.Layer(gpaths_r, ex, feed)
layer_l = g.Layer(gpaths_l, ex, feed)
layer.cuttingConfig(cut, mergin)
layer_r.cuttingConfig(cut, mergin)
layer_l.cuttingConfig(cut, mergin)

model = g.Model(settings, printer, extrusion_symbol='U', oneStrokeMode=True)

for i in range(30):
    model.stack(layer, h*i+0.025)
    if i < 3:
        model.stack(layer_r, h*i+0.025)
        model.stack(layer_l, h*i+0.025)

model.generate('gcodes/SH0125T0.gcode')