#!/bin/bash

mv *.log *.hlt ./logs/
~/Projects/Halite/environment/halite \
-d "30 30" \
"docker run -i --rm ghcr.io/nmalaguti/halite-bots/easybot:sha-af66315" \
"python3 Trent.py"
