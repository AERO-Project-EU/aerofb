#
# ckatsak, Wed Mar 13 02:12:20 PM EET 2024
#
DOCKER ?= docker
IMG := aerofb-alpine-flask
TAG := 0.0.1

.PHONY: $(IMG) clean
$(IMG):
	# NOTE: Assuming `docker login` has already been called
	$(DOCKER) buildx build \
		--progress=plain \
		--no-cache \
		--pull \
		--platform linux/amd64,linux/arm64/v8 \
		--push \
		--build-arg AERO_FB_TAG=$(TAG) \
		--tag ckatsak/$(IMG):$(TAG) \
		.
clean:
	$(DOCKER) rmi ckatsak/$(IMG):$(TAG)

