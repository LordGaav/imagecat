KEY=CD9C0E84
DIST=saucy

changelog:
	git dch --ignore-branch --snapshot --auto --git-author

release:
	git dch --ignore-branch --release --auto -N $(VERSION) --git-author

package:
	dpkg-buildpackage -A -us -uc

source:
	dpkg-buildpackage -S -k$(KEY)

source_no_sign:
	dpkg-buildpackage -S -us

upload_to_ppa:
	dput ppa:lordgaav/vsphere-client "$(CHANGES)"

pbuild:
	pbuilder-dist "$(DIST)" "$(CHANGES)"
