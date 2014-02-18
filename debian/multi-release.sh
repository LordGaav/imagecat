#!/bin/bash

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
CYAN=$(tput setaf 6)
WHITE=$(tput setaf 7)
NORMAL=$(tput sgr0)

echo_red() {
	echo -e "${RED}${1}${NORMAL}"
}

## Make sure we execute from within the debian folder
if [ -L "$0" ]; then
	CMD="$(readlink -f "$0")"
else
	CMD="$0"
fi

BASE=$(dirname $CMD)

echo_red "Changing to debian control dir"
pushd $BASE

## Determine targeted distributions
DISTS=$(ls -1 control.* | sed "s#control\.##")
SUFFIX="1"

echo_red "Found distributions: "$DISTS

for i in $DISTS; do
	if [ "$i" == "source" ]; then
		continue
	fi
	## Create control file for distribution
	echo_red "Creating control file for $i"

	rm control 2>/dev/null
	cat control.source control.$i > control

	## Modify changelog
	echo_red "Modifying changelog"
	mv changelog changelog.orig
	sed "0,/) RELEASE/{
		s#) RELEASE#-${i}${SUFFIX}) ${i}#;
	};
	s#RELEASE#${i}#;" changelog.orig > changelog

	## Build source package
	(cd .. && make -f debian/Makefile source)

	## Revert changelog
	echo_red "Cleaing up"
	git checkout changelog
done

popd
