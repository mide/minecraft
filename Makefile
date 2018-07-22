build:
	docker build -t mide/minecraft:latest -f Dockerfile .
	docker tag "mide/minecraft:latest" "mide/minecraft:${TRAVIS_COMMIT}"
	docker tag "mide/minecraft:latest" "mide/minecraft:$(shell date +%Y-%m)"

push:
	@make build
	echo "${DOCKER_HUB_PASSWORD}" | docker login -u "${DOCKER_HUB_USERNAME}" --password-stdin
	docker push "mide/minecraft:latest"
	docker push "mide/minecraft:${TRAVIS_COMMIT}"
	docker push "mide/minecraft:$(shell date +%Y-%m)"
