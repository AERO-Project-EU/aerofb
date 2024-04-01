#
# ckatsak, Thu Mar 14 04:08:46 AM EET 2024
#
DOCKER ?= docker

REGISTRY = ghcr.io
OWNER ?= ckatsak
IMG_PREFIX := aerofb
TAG ?= 0.0.1

BENCHES := $(wildcard benches/*)


.PHONY: all
all: benches

###############################################################################

.PHONY: benches $(BENCHES)
benches: $(BENCHES)
$(BENCHES):
	-ln server.py $(wildcard $</*.py) $@
	$(DOCKER) buildx build \
		--progress=plain \
		--no-cache \
		--pull \
		--platform linux/amd64,linux/arm64/v8 \
		--push \
		-f $@/Dockerfile \
		-t $(REGISTRY)/$(OWNER)/$(IMG_PREFIX)-$(shell basename $@):$(TAG) \
		$@

.PHONY: base-images
base-images:
	$(MAKE) -C $@/alpine-base
	$(MAKE) -C $@/alpine-flask

###############################################################################

.PHONY: clean clean-images distclean

clean:
	@$(RM) -v $(shell find benches -name 'server.py')

clean-images:
	-@for d in $(shell ls benches); do \
		$(DOCKER) rmi $(REGISTRY)/$(OWNER)/$(IMG_PREFIX)-$$d:$(TAG); \
	done

distclean: clean clean-images

