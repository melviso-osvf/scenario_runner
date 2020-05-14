#!/usr/bin/env groovy

String CARLA_HOST 
String CARLA_RELEASE
String TEST_HOST

pipeline
{
    agent none

    options
    {
        buildDiscarder(logRotator(numToKeepStr: '3', artifactNumToKeepStr: '3'))
        skipDefaultCheckout()
    }

    stages
    {
        stage('setup')
        {
            agent { label "master" }
            steps
            {
                checkout scm
                script
                {
                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    TEST_HOST = jenkinsLib.getUbuntuTestNodeHost()
                    CARLA_HOST= sh(
                        script: "cat ./CARLA_VER | grep HOST | sed 's/HOST\\s*=\\s*//g'",
                        returnStdout: true).trim()
                    CARLA_RELEASE = sh(
                        script: "cat ./CARLA_VER | grep RELEASE | sed 's/RELEASE\\s*=\\s*//g'",
                        returnStdout: true).trim()
                }
                println "using CARLA version ${CARLA_RELEASE} from ${TEST_HOST}"
            }
        }
        stage('build docker image')
        {
            agent { label "master" }
            steps
            {
                //checkout scm
                sh 'docker build -t jenkins/scenario_runner .'
                sh 'docker tag jenkins/scenario_runner 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
                sh '$(aws ecr get-login | sed \'s/ -e none//g\' )' 
                sh 'docker push 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
            }
        }
        stage('deploy & test')
        {
            stages
            {
                stage('start CARLA')
                {
                    stages
                    {
                        stage('start test node')
                        {
                            agent { label "master" }
                            steps
                            {
                                script
                                {
                                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                                    jenkinsLib.StartUbuntuTestNode()
                                }
                            }
                        }
                        stage('install CARLA')
                        {
                            agent { label "slave && ubuntu && gpu && sr" }
                            steps
                            {
                                println "using CARLA version ${CARLA_RELEASE}"
                                sh "wget -qO- ${CARLA_HOST}/${CARLA_RELEASE}.tar.gz | tar -xzv -C ."
                            }
                        }
                    }
                }
                stage('run tests')
                {
                    parallel
                    {
                        stage('deploy carla')
                        {
                            agent { label "slave && ubuntu && gpu && sr" }
                            options {
                                timeout(time: 10, unit: 'MINUTES') 
                            }
                            steps
                            {
                                sh 'DISPLAY= ./CarlaUE4.sh -opengl -nosound > CarlaUE4.log'
                            }
                        }
                        stage('basic test')
                        {
                            agent { label "master"}
                            options {
                                timeout(time: 10, unit: 'MINUTES') 
                            }                            
                            steps
                            {
                                script
                                {
                                    sh 'sleep 10'
                                    sh '$(aws ecr get-login | sed \'s/ -e none//g\' )' 
                                    sh 'docker container prune -f'
                                    sh "docker container run --rm --network host \"jenkins/scenario_runner\" -c \"python3 scenario_runner.py --scenario FollowLeadingVehicle_1 --host ${TEST_HOST} --debug --output --reloadWorld \""
                                }
                                script
                                {
                                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                                    jenkinsLib.StopUbuntuTestNode()
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post
    {
        always
        {
            node('master')
            {
                script  
                {
                    // jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    // jenkinsLib.StopUbuntuTestNode()
                    echo 'test node stopped'
                    sh 'docker system prune --volumes -f'
                }
                deleteDir()
            }
        }
    }
}
