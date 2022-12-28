<h1 align=center>gmake</h1>

> This is code for paper "Improvement of mechanical properties of 3D-printed continuous carbon fiber reinforced polymers by fiber tensioning and compaction during printing."

## Reproducibility
### Environment
This source code depends on the following external software and python3. To enforce reproducibility of our study, we recommend to use our container.
The container is based on Ubuntu20.04 with python3.8, and following libraries have been installed:

* [svgpathtools](https://github.com/mathandy/svgpathtools)
* [tsp-solver](https://github.com/dmishin/tsp-solver)
* [numpy](https://github.com/numpy/numpy)

The container was stored in docker hub repository, [gmake](https://hub.docker.com/repository/docker/ichiharanaruki/gmake).
First, clone this github repository on your local host
```bash
git clone https://github.com/Naruki-Ichihara/gmake.git
```
then move to `.docker_gmake` and run the docker-compose.
```bash
cd .docker_gmake && docker-compose up
```
Finally, you should install this repository in the docker image.
```
pip install git+https://github.com/Naruki-Ichihara/g-maker-fiber.git@main
```

### Usage
To generate G-code for each specimens, please run the python file that named specimens code.
The specimens code was follows the following rule.
```
IdenficationChalacter_LayerHeight_TensionRate.py
```

* S: Standard specimen
* T: Tensioning specimen
* C: Compression specimen
* TC: Tensionig and Compression specimen

For exapmple, 25% compression with 4% tensioning code as follows:
```
TC_H01_T4.py
```
