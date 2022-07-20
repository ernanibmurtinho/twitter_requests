PYTHON=$(shell which python)

#################################################################################
# Clean	                                                                        #
#################################################################################
clean:
	rm -rf .pytest_cache
	rm -rf dist

#################################################################################
# Build pex                                                                     #
#################################################################################
build: clean
	mkdir -p dist
	pex . -v --disable-cache -r requirements.txt -D twitter_ingestion/docs -o dist/twitter_ingestion.pex --python=$(PYTHON)

#################################################################################
# Run pex                                                                     #
#################################################################################
run:
	$(PYTHON) dist/twitter_ingestion.pex -m twitter_ingestion.main --retrieveTweets run

#################################################################################
# Execute the build Docker                                                      #
#################################################################################
docker:
	rm -rf out
	DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker build . --target=result --output out

#################################################################################
# Deploy to prodution		                                                    #
#################################################################################
deploy-prod: docker
