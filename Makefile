TOPDIR=$(shell pwd)
DATE="date +%Y%m%d"
PROGRAMNAME=msi-collectl
RELEASE=3.6.0
TMPDIR=/tmp
BUILDDIR=build

all: rpms

build: clean
	echo $(TOPDIR)
#echo "- Create changelog file"
#git shortlog > changelog.txt
	echo "- Create new $(TMPDIR)/$(BUILDDIR)"
	mkdir -p $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)
	echo "- Copy sources"
	rsync -raC --exclude .git . $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME)	
	echo "- Compressing $(PROGRAMNAME) directory"
	tar -czf $(PROGRAMNAME)-$(RELEASE).tar.gz -C $(TMPDIR)/$(BUILDDIR) $(PROGRAMNAME)/
	echo "- Moving source package in dist dir"
	mkdir -p ./dist
	mv $(PROGRAMNAME)-$(RELEASE).tar.gz ./dist

clean:
	-rm -rf dist/
	-rm -rf rpm-build*
	-rm -rf $(TMPDIR)/$(BUILDDIR)

sdist: messages

rpms: build
	for os in fedora suse; do \
		cp -r $(TMPDIR)/$(BUILDDIR)/$(PROGRAMNAME) rpm-build-$$os ; \
		cp dist/*.gz rpm-build-$$os/ ; \
		rpmbuild --define "_topdir %(pwd)/rpm-build-$$os" \
			--define "_builddir %{_topdir}" \
			--define "_rpmdir %{_topdir}" \
			--define "_srcrpmdir %{_topdir}" \
			--define '_rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm' \
			--define "_specdir %{_topdir}" \
			--define "_sourcedir  %{_topdir}" \
			--define "_for_os $$os" \
			-ba msi-collectl.spec ;\
	done