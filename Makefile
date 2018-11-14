test:
		docker run -i --mount type=bind,source=${PWD}/tests,target=/app/tests --mount type=bind,source=${PWD}/lambdas,target=/app/lambdas  --mount type=bind,source=${PWD}/src,target=/app/src -t mdm  python -m unittest discover tests
