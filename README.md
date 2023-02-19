<h1 align=center>gmake</h1>

## Reproducibility
### Environment
This source code depends on the following external software and python3. To enforce the reproducibility of our study, we recommend using our container.
The container is based on Ubuntu20.04 with python3.8, and the following libraries have been installed:

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

### Usage
To generate the G-code for each specimen, please run the python file that is named specimens code.
The specimens' code follows the following rule.
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
