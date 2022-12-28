import gmaker as g
from svgpathtools import Path, Line

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
h = 0.1

# Read svg file
paths = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        paths.append(Path(Line((20+50j)+(0+shift*1j), (240+50j)+(0+shift*1j))))
    else:
        paths.append(Path(Line((240+50j)+(0+shift*1j), (20+50j)+(0+shift*1j))))
# Convert paths bezier to lines
paths = g.paths2LinePaths(paths, division=200, sorting=False)

anchor_paths_r = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        anchor_paths_r.append(Path(Line((20+40j)+(shift*1+0j), (20+73j)+(shift*1+0j))))
    else:
        anchor_paths_r.append(Path(Line((20+73j)+(shift*1+0j), (20+40j)+(shift*1+0j))))
anchor_paths_r = g.paths2LinePaths(anchor_paths_r, division=200, sorting=False)
        
anchor_paths_l = []
for i in range(13):
    shift = 1.0*i
    if i%2 == 0:
        anchor_paths_l.append(Path(Line((240+73j)-(shift*1+0j), (240+40j)-(shift*1+0j))))
    else:
        anchor_paths_l.append(Path(Line((240+40j)-(shift*1+0j), (240+73j)-(shift*1+0j))))
anchor_paths_l = g.paths2LinePaths(anchor_paths_l, division=200, sorting=False)

# Position wise values
ex = lambda x, y: 1.0*asynchronousRate   # Extrusion map
feed = lambda x, y: 600 # Feedrate map

# svg paths to gPath class list
gpaths = [g.gPath(path) for path in paths]
gpaths_r = [g.gPath(path) for path in anchor_paths_r]
gpaths_l = [g.gPath(path) for path in anchor_paths_l]

# Set primary layer
layer = g.Layer(gpaths, ex, feed)
layer_r = g.Layer(gpaths_r, ex, feed)
layer_l = g.Layer(gpaths_l, ex, feed)
layer.cuttingConfig(cut, mergin)
layer_r.cuttingConfig(cut, mergin)
layer_l.cuttingConfig(cut, mergin)

# Set model with printer setting
model = g.Model(settings, printer, extrusion_symbol='U', oneStrokeMode=True)

# Stacking 100 plies
for i in range(30): #12
    model.stack(layer, h*i+0.025)
    if i < 3:
        model.stack(layer_r, h*i+0.025)
        model.stack(layer_l, h*i+0.025)

# Generate g-code
model.generate('gcodes/TCH01T4.gcode')