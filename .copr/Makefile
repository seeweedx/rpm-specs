# COPR's make_srpm method runs `make -f .copr/Makefile srpm outdir=... spec=...`
# for each package: fetch the remote sources its spec names, copy the patches
# kept beside it, then pack them.
srpm:
	dnf -y install rpmdevtools
	spectool -g -C $(outdir) $(spec)
	find $(dir $(spec)) -maxdepth 1 -name '*.patch' -exec cp -t $(outdir) {} +
	rpmbuild -bs --define '_sourcedir $(outdir)' --define '_srcrpmdir $(outdir)' $(spec)
