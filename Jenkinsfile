#!/usr/bin/env groovy

String CARLA_HOST 
String CARLA_RELEASE

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
                    CARLA_HOST= sh(
                        script: "cat ./CARLA_VER | grep HOST | sed 's/HOST\\s*=\\s*//g'",
                        returnStdout: true).trim()
                    CARLA_RELEASE = sh(
                        script: "cat ./CARLA_VER | grep RELEASE | sed 's/RELEASE\\s*=\\s*//g'",
                        returnStdout: true).trim()
                }
                println "using CARLA version ${CARLA_RELEASE}"
            }
        }
        /** commented while testing setup of test node
        stage('build')
        {
            agent { label "master" }
            steps
            {
                checkout scm
                sh 'docker build -t jenkins/scenario_runner .'
                sh 'docker tag jenkins/scenario_runner 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
                sh '$(aws ecr get-login | sed \'s/ -e none//g\' )' 
                sh 'docker push 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
            }
        }
        **/
        stage('start server')
        {
            agent { label "master" }
            steps
            {
                println "start server node"
                script
                {
                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    jenkinsLib.StartUbuntuTestNode()
                    sh 'echo server started!'
                }
            }
        }
        stage('deploy carla')
        {
            agent { label "slave && ubuntu && gpu && sr" }
            steps
            {
                println "get $CARLA_HOST/$CARLA_RELEASE.tar.gz"
                sh 'wget -qO- $CARLA_HOST/$CARLA_RELEASE.tar.gz | tar -xzv -C Dist/'
                sh 'DISPLAY= ./Dist/CarlaUE4.sh -opengl --carla-rpc-port=3654 --carla-streaming-port=0 -nosound > CarlaUE4.log &'
                sh 'make smoke_tests ARGS="--xml"'
                sh 'make run-examples ARGS="localhost 3654"'
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
                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    jenkinsLib.StopUbuntuTestNode()
                }
                deleteDir()
            }
        }
    }
}
