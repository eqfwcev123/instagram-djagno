#!/usr/bin/env python
import subprocess

DOCKER_IMAGE_TAG='eqfwcev123/docker-wps12'

subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)
subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)