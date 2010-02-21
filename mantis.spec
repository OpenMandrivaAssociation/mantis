%define	name	mantis
%define oname   mantisbt
%define	version	1.1.8
%define	release	%mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Web-based bug tracker
License:	GPL
Group:		System/Servers
URL:		http://www.mantisbt.org
Source0:	%{oname}-%{version}.tar.gz
Source1:	%{name}-apache.conf.bz2
Requires:   apache-mod_php
Requires:	php-mysql
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

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
rm -rf  %{buildroot}

rm -rf packages
# install files
install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%_defaultdocdir/%{name}-%{version}
mv doc/*  %{buildroot}%_defaultdocdir/%{name}-%{version}
rm -rf doc
cp -aRf * %{buildroot}%{_var}/www/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf

find %{buildroot}%{_var}/www/%{name} -name '*.php' -exec perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|g' {} \;

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%_defaultdocdir/%{name}-%{version}
%{_var}/www/%{name}
