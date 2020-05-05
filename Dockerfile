from ubuntu:18.04

# install base libs
run apt-get update && apt-get install --no-install-recommends -y \
    libpng16-16 libtiff5 libjpeg8 build-essential wget git python3.6 python3.6-dev python3-pip 

# install python dependencies 
run pip3 install --user setuptools wheel py_trees==0.8.3 networkx==2.2 pygame==1.9.6 \
    six==1.14.0 numpy==1.18.4 psutil shapely xmlschema \
&& mkdir -p /app/scenario_runner && mkdir -p /app/carla

# install scenario_runner 
add . /app/scenario_runner

# get carla libs
env CARLA_HOST $(export $(cat CARLA_VER|grep HOST) && echo $HOST)
env CARLA_RELEASE $(export $(cat CARLA_VER|grep RELEASE) && echo $RELEASE)

run wget "${CARLA_HOST}/${CARLA_RELEASE}.tgz" && tar -xzvf "${CARLA_RELEASE}.tar.gz" 
add PythonAPI/carla /app/carla
run python3 -m easy_install $(find /app/carla/ -iname "*py3.6*.egg" )
env PYTHONPATH "${PYTHONPATH}:/app/carla/agents:/app/carla"
workdir /app/scenario_runner
# entrypoint ["/bin/sh" ]

