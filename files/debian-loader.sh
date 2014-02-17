#!/bin/sh
while :
do
	# When gnome exits, our parent process becomes init,
	# but the PPID stays set.
	if ! ps -p $PPID > /dev/null
	then
		exit 0
	fi
	/usr/bin/imagecat --quiet --automatic
	sleep 120
done
