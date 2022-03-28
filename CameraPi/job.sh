#!/bin/bash
    # Read the stdout of ./lora
	./lora | while read -r line; do
      # if ./lora prints "Start detection",
	  if [ "$line" = "Start detection" ];
	  then
	    python3 ./integrated/integrated.py

      # else if ./lora prints "Session finished"
	  elif [ "$line" = "Session finished" ];
	  then
	    echo "Sending (Compressed, Warped) Image.."
	    continue
	 
      # else if ./lora prints "Shutdown"
	  elif [ "$line" = "Shutdown" ];
	  then
		shutdown now

      # else if ./lora prints ""
	  elif [ "$line" = "" ];
	  then
		  continue

      # else if ./lora prints other unexpected behavior
	  else
		  continue
	  
	  fi  
	echo "Reading another signal..."
	done
