#!/bin/sh
set +e

echo "Reloading imagecat config..."
killall -USR1 imagecat &&
echo "Done reloading"
