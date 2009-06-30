%define	name	mantis
%define oname   mantisbt
%define	version	1.1.8
%define	release	%mkrel 1
%define order	71

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Web-based bug tracker
License:	GPL
Group:		System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mantisbt.org
Source0:	%{oname}-%{version}.tar.gz
Source1:	%{name}-apache.conf.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= 2.0.54
Requires(pre):  apache-mpm >= 2.0.54
Requires:       apache-mod_php
Requires:	MySQL
BuildArch:	noarch
BuildRequires:	file

%description
Mantis is a php/MySQL/web based bugtracking system.
The goals for this project are to produce and maintain a
lightweight and simple bugtracking system. Additions of
complexity and/or features are modular and configurable
so that users can be shielded from unwanted clutter.

The product is designed to be easily modifiable,
customizable, and upgradeable. Anyone with intermediate
PHP and MySQL experience should be able to customize
Mantis to suit their needs.

%prep
%setup -q -n %{oname}-%{version}

%build

%install
rm -rf  $RPM_BUILD_ROOT

rm -rf packages
# install files
install -d -m 755 $RPM_BUILD_ROOT%{_var}/www/%{name}
install -d -m 755 $RPM_BUILD_ROOT%_defaultdocdir/%{name}-%{version}
mv doc/*  $RPM_BUILD_ROOT%_defaultdocdir/%{name}-%{version}
rm -rf doc
cp -aRf * $RPM_BUILD_ROOT%{_var}/www/%{name}

# apache configuration
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/webapps.d
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/webapps.d/%{order}_%{name}.conf

find $RPM_BUILD_ROOT%{_var}/www/%{name} -name '*.php' -exec perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|g' {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{order}_%{name}.conf
%_defaultdocdir/%{name}-%{version}
%{_var}/www/%{name}/*.php
%{_var}/www/%{name}/*.sample
%{_var}/www/%{name}/admin
%{_var}/www/%{name}/core
%{_var}/www/%{name}/css
%{_var}/www/%{name}/graphs
%{_var}/www/%{name}/images
%{_var}/www/%{name}/javascript
%{_var}/www/%{name}/lang
%{_var}/www/%{name}/api/*
