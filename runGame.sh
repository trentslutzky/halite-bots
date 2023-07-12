#!/bin/bash

mv *.log *.hlt ./logs/
~/Projects/Halite/environment/halite \
-d "30 30" \
"python3 overkill_bot.py" \
"python3 Trent.py"
