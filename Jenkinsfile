pipeline {
  agent any
  stages {
    stage('build nodes') {
      steps {
      	docker.imagen('ubuntu:18.04').inside(
		apt-get update && apt-get install --no-install-recommends -y python3.6 python3-pip build-essential
		apt-get install --no-install-recommends -y git
		apt-get install --no-install-recommends -y python3-dev
		pip3 install --user setuptools wheel && pip3 install --user py_trees==0.8.3 networkx==2.2 psutil shapely xmlschema && mkdir -p /app/scenario_runner && mkdir -p /app/carla
		git clone --depth 1 -b master https://github.com/melviso-osvf/scenario_runner.git /app/scenario_runner
		wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.8.tar.gz && tar -xzvf CARLA_0.9.8.tar.gz 
		cp -rf  PythonAPI/carla /app/carla
		sh /app/dist/carla-0.9.8-py3.5-linux-x86_64.egg
		export PYTHONPATH="${PYTHONPATH}:/app/carla/agents:/app/carla"
		/app/scenario_runner
		/bin/bash -c "python3.6 scenario_runner --scenario group:FollowLeadingVehicle"
      }
    }

  }
}
