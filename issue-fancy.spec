Summary:	PLD Linux release file with logo
Summary(de):	PLD Linux Release-Datei mit logo
Summary(pl):	Wersja Linuksa PLD z logiem
Name:		issue-fancy
Version:	1.0
Release:	3
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Source0:	%{name}-gen
Source1:	%{name}.crontab
Source2:	%{name}.sysconfig
Requires:	crondaemon
# In fact it requires quote_logo_backslashes patch.
Requires:	linux_logo >= 3.9b5
BuildArch:	noarch
Obsoletes:	redhat-release
Obsoletes:	mandrake-release
Obsoletes:	issue
Obsoletes:	issue-pure
Obsoletes:	issue-logo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PLD Linux release file with logo.

%description -l pl
Wersja Linuksa PLD z logiem.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{cron.d,rc.d/init.d},/sbin}

install %{SOURCE0} $RPM_BUILD_ROOT/sbin
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/issue-fancy

$RPM_BUILD_ROOT/sbin/issue-fancy-gen $RPM_BUILD_ROOT

echo "1.0 PLD Linux (Ra)" > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

%post
/sbin/issue-fancy-gen

if [ "$1" != "0" ]; then
	/sbin/chkconfig --add issue-fancy
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del issue-fancy
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_sysconfdir}/pld-release
# Can't use "noreplace" here because issues are regenerated from cron
# and %post. Without "noreplace" at least ".rpmsave" will stay.
%config %{_sysconfdir}/issue*
%attr(755,root,root) /sbin/*
%attr(600,root,root) /etc/cron.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
