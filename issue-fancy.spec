Summary:	PLD Linux release file with logo
Summary(de):	PLD Linux Release-Datei mit logo
Summary(pl):	Wersja Linuksa PLD z logiem
Name:		issue-fancy
Version:	1.0
Release:	6
License:	GPL
Group:		Base
Group(cs):	Základ
Group(da):	Basal
Group(de):	Basis
Group(es):	Base
Group(fr):	Base
Group(is):	Grunnforrit
Group(it):	Base
Group(ja):	¥Ù¡¼¥¹
Group(no):	Basis
Group(pl):	Podstawowe
Group(pt):	Base
Group(pt_BR):	Base
Group(ru):	âÁÚÁ
Group(sl):	Osnova
Group(sv):	Bas
Group(uk):	âÁÚÁ
Source0:	%{name}-gen
Source1:	%{name}.crontab
Source2:	%{name}.init
# In fact it requires quote_logo_backslashes patch.
BuildRequires:	linux_logo >= 3.9b5
Requires:	crondaemon
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
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/issue-fancy

$RPM_BUILD_ROOT/sbin/issue-fancy-gen $RPM_BUILD_ROOT

echo "1.0 PLD Linux (Ra)" > $RPM_BUILD_ROOT%{_sysconfdir}/pld-release

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
%attr(755,root,root) /sbin/*
%attr(600,root,root) /etc/cron.d/*
%attr(754,root,root) /etc/rc.d/init.d/*
