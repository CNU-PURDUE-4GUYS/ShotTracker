#!/bin/bash
while true; do
	./lora | while read -r line; do
	  if [ "$line" = "Start detection" ] 
	  then
	    # need to make variable 'line' empty for preventing buffer issues. It may cause unexpected iteration as buffer is filled.
	    echo "start! $line"
	    python3 ./integrated/integrated.py

	  elif [ "$line" = "Session finished" ] 
	  then
	    python3 ./sendImage.py
	    break
	 
	  elif [ "$line" = "Shutdown" ]
	  then
		python3 test.py
	  else 
		continue

	  fi  
	done
done
