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
%if %{_for_os} == "fedora"
Requires: dmidecode
%endif

%description
A fork of collectl tailored for MSI.

%install


DESTDIR=$RPM_BUILD_ROOT
BINDIR=$DESTDIR/usr/bin
DOCDIR=$DESTDIR/usr/share/doc/collectl
SHRDIR=$DESTDIR/usr/share/collectl
MANDIR=$DESTDIR/usr/share/man/man1
ETCDIR=$DESTDIR/etc
%if %{_for_os} == "fedora"
INITPATH=/etc/rc.d/init.d
INITFILE=collectl
%elseif %{_for_os} == "suse"
INITPATH=/etc/init.d
INITFILE=collectl-suse
%endif
INITDIR=$DESTDIR/$INITPATH

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

#%{__rm} -f $INITDIR/collectl-suse
#%{__rm} -f $INITDIR/collectl-debian
#%{__rm} -f $INITDIR/collectl-generic

install -m 755 initd/$INITFILE $INITDIR/collectl

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/*/*

%config /etc/collectl.conf

%if %{_for_os} == "fedora"
%attr(0755, root, root) /etc/rc.d/init.d/collectl
%elseif %{_for_os} == "suse"
%attr(0755, root, root) /etc/init.d/collectl
%endif
%attr(0444, root, root) /etc/collectl.conf
%attr(0755, root, root) /usr/bin/collectl
%attr(0444, root, root) /usr/share/doc/collectl/*
%attr(0755, root, root) /usr/share/collectl/util/client.pl
%attr(0755, root, root) /usr/share/collectl/util/readS
%attr(0755, root, root) /usr/share/collectl/util/col2tlviz.pl
%attr(0444, root, root) /usr/share/collectl/*.ph

%pre

%post
if [ -x /usr/lib/lsb/install_initd ]; then
  /usr/lib/lsb/install_initd /etc/init.d/collectl
elif [ -x /sbin/chkconfig ]; then
  /sbin/chkconfig --add collectl
else
   for i in 2 3 4 5; do
        ln -sf /etc/init.d/collectl /etc/rc.d/rc${i}.d/S11collectl
   done
   for i in 1 6; do
        ln -sf /etc/init.d/collectl /etc/rc.d/rc${i}.d/K01collectl
   done
fi

%prerun
#only on uninstall, not on upgrades.
if [ $1 = 0 ]; then
  /etc/init.d/collectl stop  > /dev/null 2>&1
  if [ -x /usr/lib/lsb/remove_initd ]; then
    /usr/lib/lsb/install_initd /etc/init.d/collectl
  elif [ -x /sbin/chkconfig ]; then
    /sbin/chkconfig --del collectl
  else
    rm -f /etc/rc.d/rc?.d/???collectl
  fi
fi