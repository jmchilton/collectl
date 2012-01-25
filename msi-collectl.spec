Summary: MSI Collectl
Name: msi-collectl
Version: 3.6.0
Release: 1
License: GPL
Group: Applications/System
URL: https://github.com/jmchilton/collectl
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
A fork of collectl tailored for MSI.

%install
DESTDIR=$RPM_BUILD_ROOT
BINDIR=$DESTDIR/usr/bin
DOCDIR=$DESTDIR/usr/share/doc/collectl
SHRDIR=$DESTDIR/usr/share/collectl
MANDIR=$DESTDIR/usr/share/man/man1
ETCDIR=$DESTDIR/etc
INITDIR=$ETCDIR/init.d

%{__mkdir} -p $BINDIR
%{__mkdir} -p $DOCDIR
%{__mkdir} -p $SHRDIR
%{__mkdir} -p $ETCDIR
%{__mkdir} -p $MANDIR
%{__mkdir} -p $INITDIR
%{__mkdir} -p $SHRDIR/util
%{__mkdir} -p $DESTDIR/var/log/collectl

%{__cp} collectl.pl           $BINDIR/collectl
%{__cp} collectl.conf         $ETCDIR
%{__cp} man1/*                $MANDIR
%{__cp} initd/*               $INITDIR

%{__cp} docs/*                $DOCDIR
%{__cp} GPL ARTISTIC COPYING  $DOCDIR
%{__cp} RELEASE-collectl      $DOCDIR

%{__cp} UNINSTALL             $SHRDIR
%{__cp} formatit.ph           $SHRDIR
%{__cp} lexpr.ph sexpr.ph     $SHRDIR
%{__cp} gexpr.ph misc.ph      $SHRDIR
%{__cp} envrules.std          $SHRDIR
%{__cp} vmstat.ph             $SHRDIR
%{__cp} client.pl readS       $SHRDIR/util
%{__cp} col2tlviz.pl          $SHRDIR/util

gzip -f $MANDIR/collectl*

# remove any stale versions in case the names/numbers used have changed.
# on new ROCKS installion 'rm' isn't there yet!  [thanks roy]
if [ -x /bin/rm ] ; then
  /bin/rm -f $INITDIR/rc*.d/*collectl
  /bin/rm -f $ETCDIR/rc.d/rc*.d/*collectl
fi

# Try and decide which distro this is based on distro specific files.
distro=1
if [ -f /sbin/yast ]; then
    distro=2
    mv -f $INITDIR/collectl-suse $INITDIR/collectl
    rm -f $INITDIR/collectl-debian
    rm -f $INITDIR/collectl-generic
fi

# debian
if [ -f /usr/sbin/update-rc.d ]; then
    distro=3
    mv -f $INITDIR/collectl-debian $INITDIR/collectl
    rm -f $INITDIR/collectl-suse
    rm -f $INITDIR/collectl-generic

    # only if we're installing under /
    [ "$DESTDIR" = "/" ] && update-rc.d collectl defaults
fi

# redhat
if [ -f /etc/redhat-release ]; then
    distro=4
    rm -f $INITDIR/collectl-suse
    rm -f $INITDIR/collectl-debian
    rm -f $INITDIR/collectl-generic
    [ "$DESTDIR" = "/" ] && chkconfig --add collectl
fi

# gentoo
if [ -f $ETCDIR/gentoo-release ]; then
    distro=5
    mv -f $INITDIR/collectl-generic $INITDIR/collectl
    rm -f $INITDIR/collectl-suse
    rm -f $INITDIR/collectl-debian
    [ "$DESTDIR" = "/" ] && rc-update -a collectl default
fi



%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/*/*

%config /etc/collectl.conf
%attr(0755, root, root) /etc/init.d/collectl*
%attr(0444, root, root) /etc/collectl.conf
%attr(0755, root, root) /usr/bin/collectl
%attr(0444, root, root) /usr/share/doc/collectl/*
%attr(0755, root, root) /usr/share/collectl/util/client.pl
%attr(0755, root, root) /usr/share/collectl/util/readS
%attr(0755, root, root) /usr/share/collectl/util/col2tlviz.pl
%attr(0444, root, root) /usr/share/collectl/*.ph

%pre

%post
