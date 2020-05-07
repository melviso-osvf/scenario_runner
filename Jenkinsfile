#!/usr/bin/env groovy

pipeline
{
    agent none

    options
    {
        buildDiscarder(logRotator(numToKeepStr: '3', artifactNumToKeepStr: '3'))
    }

    stages
    {
        parallel
        {
            stage('Building image')
            {
                agent { label "master" }
                steps
                {
                    sh 'docker build -t jenkins/scenario_runner .'
                    sh 'docker tag jenkins/scenario_runner 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
                    sh '$(aws ecr get-login | sed \'s/ -e none//g\' )' 
                    sh 'docker push 456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner'
                }
            }
            stage('Creating test node') 
            {
                agent { label "master" }
                steps
                {
                    JOB_ID = "${env.BUILD_TAG}"
                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    jenkinsLib.CreateUbuntuTestNode(JOB_ID)
                }
            }
        }
    }
    post
    {
        always
        {
            deleteDir()
            node('master')
            {
                script
                {
                    JOB_ID = "${env.BUILD_TAG}"
                    jenkinsLib = load("/home/jenkins/scenario_runner.groovy")
                    jenkinsLib.DeleteUbuntuTestNode(JOB_ID)
                }
            }
        }
    }
}
