Summary:	PLD Linux release file with logo
Summary(de):	PLD Linux Release-Datei mit logo
Summary(pl):	Wersja Linuksa PLD z logiem
Name:		issue-fancy
Version:	1.99
Release:	1
License:	GPL
Group:		Base
Source0:	%{name}-gen
Source1:	%{name}.crontab
Source2:	%{name}.init
# In fact it requires quote_logo_backslashes patch.
BuildRequires:	linux_logo >= 3.9b5
Requires:	linux_logo >= 3.9b5
Requires:	crondaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	redhat-release
Obsoletes:	mandrake-release
Obsoletes:	issue
Obsoletes:	issue-alpha
Obsoletes:	issue-logo
Obsoletes:	issue-pure

%define		_sbindir	/sbin

%description
PLD Linux release file with logo.

%description -l pl
Wersja Linuksa PLD z logiem.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d},%{_sbindir}}

install %{SOURCE0} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/issue-fancy

$RPM_BUILD_ROOT%{_sbindir}/issue-fancy-gen $RPM_BUILD_ROOT

echo "1.99 PLD Linux (Ac)" > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/issue-fancy-gen
/sbin/chkconfig --add issue-fancy

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del issue-fancy
fi

%files
%defattr(644,root,root,755)
%{_sysconfdir}/pld-release
# Can't use "noreplace" here because issues are regenerated from cron
# and %post. Without "noreplace" at least ".rpmsave" will stay.
%config %{_sysconfdir}/issue*
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) /etc/cron.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
