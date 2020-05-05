node
{
	checkout scm
	docker.withRegistry("https://456841689987.dkr.ecr.eu-west-3.amazonaws.com/scenario_runner",'ecr:eu-west-3:awscreds')
	{
		def build_image = docker.build('test/scenario_runner')
		build_image.push()
	}
}

