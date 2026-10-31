# COPR's make_srpm method runs `make -f .copr/Makefile srpm outdir=... spec=...`
# for each package: fetch the remote sources its spec names, then pack them.
srpm:
	dnf -y install rpmdevtools
	spectool -g -C $(outdir) $(spec)
	rpmbuild -bs --define '_sourcedir $(outdir)' --define '_srcrpmdir $(outdir)' $(spec)
