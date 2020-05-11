#!/usr/bin/env groovy

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
        /** commented while testing setup of test node
        stage('Building image')
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
        stage('Setup test node') 
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
        stage('carla install')
        {
            agent { label "slave && ubuntu && gpu && sr" }
            steps
            {
                script
                {
                    sh 'echo "Hello world"'
                }
            }
        }
    }
    post {
        always {
		node('master')	{
                    script  {
                        jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                        jenkinsLib.StopUbuntuTestNode()
                    }
		    deleteDir()
                }
        }
   }
}
