#!/bin/bash
#while true; do
	./lora | while read -r line; do
	echo "here: $line"
	  if [ "$line" = "Start detection" ];
	  then
	    # need to make variable 'line' empty for preventing buffer issues. It may cause unexpected iteration as buffer is filled.
	    echo "start! $line"
	    python3 ./integrated/integrated.py

	  elif [ "$line" = "Session finished" ];
	  then
	    #python3 compress.py
	    #python3 ./sendImage.py
	    continue
	 
	  elif [ "$line" = "Shutdown" ];
	  then
		python3 test.py
	  elif [ "$line" = "" ];
	  then
		  echo "asdf"
		  continue
	  
	  fi  
	echo "Reading another signal..."
	done

#done
