%define oname   mantisbt


Name:		mantis
Version:	1.2.1
Release:	6
Summary:	Web-based bug tracker
License:	GPLv2
Group:		System/Servers
URL:		https://www.mantisbt.org
Source0:	%{oname}-%{version}.tar.gz
Requires:	apache-mod_php
Requires:	php-mysql
Requires:	apache-mod_socache_shmcb
BuildArch:	noarch

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
rm -rf packages
# install files
install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%_defaultdocdir/%{name}-%{version}
mv doc/*  %{buildroot}%_defaultdocdir/%{name}-%{version}
rm -rf doc
cp -aRf * %{buildroot}%{_var}/www/%{name}

# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
Alias /mantis "/var/www/mantis"

<Directory /var/www/mantis>

    Require all granted
    
	php_admin_value memory_limit 32M
	php_admin_value max_execution_time 60
	php_admin_value register_globals Off
	php_admin_value magic_quotes_gpc Off
	php_admin_value magic_quotes_runtime Off
	# settings for the file upload, you might increase them further
	php_admin_value upload_max_filesize 16M
	# session handling: now the check for expired sessions is done on every 10th session creation
	php_admin_value session.use_trans_sid Off
	php_admin_value session.gc_probability 1
	php_admin_value session.gc_divisor 10
	# multibyte extension: needed for utf-8
	php_admin_value mbstring.func_overload 7

  <Files ~ "\.inc\.php$">
     Require all denied
   </Files>

  <Files ~ ".tpl$">
     Require all denied
  </Files>

</Directory>
EOF

find %{buildroot}%{_var}/www/%{name} -name '*.php' -exec perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|g' {} \;

%clean


%files
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%_defaultdocdir/%{name}-%{version}
%{_var}/www/%{name}


%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-2mdv2011.0
+ Revision: 612814
- the mass rebuild of 2010.1 packages

* Mon Apr 26 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.2.1-1mdv2010.1
+ Revision: 539097
- Fix license
- update to 1.2.1

* Sun Feb 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.8-2mdv2010.1
+ Revision: 509193
- use herein document for apache configuration
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

  + Thierry Vignaud <tv@mandriva.org>
    - fix description

* Tue Jun 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.8-1mdv2010.0
+ Revision: 384473
- Update to new version 1.1.8

* Fri Jan 23 2009 Jérôme Soyer <saispo@mandriva.org> 1.1.6-1mdv2009.1
+ Revision: 332765
- New upstream release

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 1.0.8-3mdv2009.0
+ Revision: 251861
- rebuild
- fix no-buildroot-tag
- kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anne Nicolas <ennael@mandriva.org> 1.0.8-1mdv2008.1
+ Revision: 120621
- add new source
- remove old source
- New version

* Mon Jun 25 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2mdv2008.0
+ Revision: 43815
- fix deps

* Sat Jun 09 2007 Anne Nicolas <ennael@mandriva.org> 1.0.7-1mdv2008.0
+ Revision: 37686
- version 1.0.7


* Mon Dec 11 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.6-1mdv2007.0
+ Revision: 95080
- Import mantis

* Mon Dec 11 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.6-1
- new version

* Mon Sep 11 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.5-1mdk
- new version

* Wed Jun 07 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.3-1mdk
- new version

* Mon Apr 24 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.2-r21mdk
- correct apache configuration

* Sat Apr 22 2006 Anne Nicolas <anne.nicolas@mandriva.com> 1.0.2-1mdk
- initial release

