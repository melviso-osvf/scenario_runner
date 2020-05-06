pipeline
{
    agent none

    options
    {
        buildDiscarder(logRotator(numToKeepStr: '3', artifactNumToKeepStr: '3'))
    }

    stages
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
    }
}
