%define		php_min_version 5.0.0
Summary:	Web-based password wallet manager
Name:		w3pw
Version:	1.40
Release:	0.14
License:	GPL v2
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/w3pw/%{name}-%{version}.tar.gz
# Source0-md5:	df718531136f3314b8582fbdd4e80791
Source1:	apache.conf
Source2:	lighttpd.conf
Source3:	init.sql
Patch0:		authpassword.patch
URL:		http://w3pw.sourceforge.net/
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	php(core) >= %{php_min_version}
Requires:	php(mcrypt)
Requires:	php(mysql)
Requires:	php(session)
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(auth)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# bad depsolver
%define		_noautopear	pear

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
w3pw is a web-based password wallet manager written in PHP. The
encrypted information is stored in a MySQL Database.

Features:
- Platform-independent: Webserver, PHP and MySQL are available for a
  wide range of Operating Systems
- Information is encrypted
- Available fields per entry: Info, Host, Login (Username), Password
  and Description
- Upload function for semicolon-delimited text-files
- Timout for automatic logout

%prep
%setup -q
%patch0 -p1

# simple sql to create and load db schema
cp -p %{SOURCE3} .

# we moved files around
%{__sed} -i -e 's,include/config.php,%{_sysconfdir}/config.php,' *.php
%{__sed} -i -e 's,include/,../include/,' *.php

# tune config
%{__sed} -i -e '
	# pld mysql root
	s,root,mysql,

	# this should be setup in php.ini
	/error_reporting/s,^,//,

	# use private tmp dir
	s#/tmp/#/var/run/php/#
' include/config.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{htdocs,sql}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

cp -a include $RPM_BUILD_ROOT%{_appdir}
cp -p *.html *.php $RPM_BUILD_ROOT%{_appdir}/htdocs
cp -p *.sql $RPM_BUILD_ROOT%{_appdir}/sql
mv $RPM_BUILD_ROOT{%{_appdir}/include,%{_sysconfdir}}/config.php

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY INSTALL
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
