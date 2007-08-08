
%define	distname	Th
%define	distversion	2.99
%define	distrelease	"%{distversion} PLD Linux (%{distname})"

Summary:	PLD Linux release file with logo
Summary(de.UTF-8):	PLD Linux Release-Datei mit logo
Summary(pl.UTF-8):	Wersja Linuksa PLD z logiem
Name:		issue-fancy
Version:	%{distversion}
Release:	3
License:	GPL
Group:		Base
Source0:	%{name}-gen
Source1:	%{name}.crontab
Source2:	%{name}.init
# In fact it requires quote_logo_backslashes patch.
BuildRequires:	linux_logo >= 3.9b5
Requires(post,preun):	/sbin/chkconfig
Requires:	linux_logo >= 3.9b5
Requires:	crondaemon
Provides:	issue
Provides:	issue-package
Obsoletes:	issue-package
Obsoletes:	redhat-release
Obsoletes:	mandrake-release
Conflicts:	issue-alpha < 2.99-2
Conflicts:	issue-logo < 2.99-2
Conflicts:	issue-pure < 2.99-5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
PLD Linux release file with logo.

%description -l pl.UTF-8
Wersja Linuksa PLD z logiem.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,rc.d/init.d},%{_sbindir}}

install %{SOURCE0} $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/issue-fancy

$RPM_BUILD_ROOT%{_sbindir}/issue-fancy-gen $RPM_BUILD_ROOT

echo %{distrelease} > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

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
