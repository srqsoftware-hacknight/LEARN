#!/bin/bash

pushd $(cd `dirname "${BASH_SOURCE[0]}"` && pwd) >> /dev/null

python -m CGIHTTPServer

popd
