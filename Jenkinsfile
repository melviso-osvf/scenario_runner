pipeline {
  agent any
  stages {
    stage('build nodes') {
      steps {
      	docker.image('ubuntu:18.04').inside{
	sh 'apt-get update && apt-get install --no-install-recommends -y python3.6 python3-pip build-essential'
	sh 'apt-get install --no-install-recommends -y git'
        sh 'apt-get install --no-install-recommends -y python3-dev'
        sh 'pip3 install --user setuptools wheel && pip3 install --user py_trees==0.8.3 networkx==2.2 psutil shapely xmlschema && mkdir -p /app/scenario_runner && mkdir -p /app/carla'
        sh 'git clone --depth 1 -b master https://github.com/melviso-osvf/scenario_runner.git /app/scenario_runner'
        sh 'wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.8.tar.gz && tar -xzvf CARLA_0.9.8.tar.gz' 
        sh 'cp -rf  PythonAPI/carla /app/carla'
        sh 'sh /app/dist/carla-0.9.8-py3.5-linux-x86_64.egg'
        sh 'export PYTHONPATH="${PYTHONPATH}:/app/carla/agents:/app/carla"'
        sh '/app/scenario_runner'
	sh 'export PYTHONPATH="${PYTHONPATH}:/app/carla/agents:/app/carla" && python3.6 scenario_runner --scenario group:FollowLeadingVehicle"'
	}
      }
    }

  }
}
