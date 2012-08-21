
%bcond_with	snap	# include shapshot information in version,
			# should be used only in official Th spanhots

%define snapshot	2012

# CPE_NAME = cpe:/ {part} : {vendor} : {product} : {version} : {update} : {edition} : {language}
# http://cpe.mitre.org/specification/
# http://csrc.nist.gov/publications/nistir/ir7695/NISTIR-7695-CPE-Naming.pdf

%if %{with snap}
%define	distname	Th/%{snapshot}
%define cpename		cpe:/o:pld-linux:pld:%{distversion}:%{snapshot}
%else
%define	distname	Th
%define cpename		cpe:/o:pld-linux:pld:%{distversion}
%endif
%define	distversion	3.0
%define	distrelease	"%{distversion} PLD Linux (%{distname})"

Summary:	PLD Linux release file with logo
Summary(de.UTF-8):	PLD Linux Release-Datei mit logo
Summary(pl.UTF-8):	Wersja Linuksa PLD z logiem
Name:		issue-fancy
Version:	%{distversion}
Release:	1%{?with_snap:.%{snapshot}}
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
Conflicts:	issue-alpha < 3.0-1
Conflicts:	issue-logo < 3.0-1
Conflicts:	issue-nice < 3.0-1
Conflicts:	issue-pure < 3.0-1
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

# CPE_NAME = cpe:/ {part} : {vendor} : {product} : {version} : {update} : {edition} : {language}
# http://cpe.mitre.org/specification/
cat >$RPM_BUILD_ROOT%{_sysconfdir}/os-release <<EOF
NAME="PLD Linux"
VERSION="%{distversion} (%{distname})"
ID="pld"
VERSION_ID="%{distversion}"
PRETTY_NAME="PLD Linux %{distversion} (%{distname})"
ANSI_COLOR="0;32"
CPE_NAME="%{cpename}"
HOME_URL="http://www.pld-linux.org/"
BUG_REPORT_URL="https://bugs.launchpad.net/pld-linux/"
EOF

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
%{_sysconfdir}/os-release
%{_sysconfdir}/pld-release
# Can't use "noreplace" here because issues are regenerated from cron
# and %post. Without "noreplace" at least ".rpmsave" will stay.
%config %verify(not md5 mtime size) %{_sysconfdir}/issue
%config %verify(not md5 mtime size) %{_sysconfdir}/issue.net
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) /etc/cron.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
