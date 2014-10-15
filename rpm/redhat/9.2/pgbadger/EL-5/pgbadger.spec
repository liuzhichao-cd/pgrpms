Summary:	a fast PostgreSQL log analyzer
Name:		pgbadger
Version:	6.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://downloads.sourceforge.net/project/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-rhel5.patch
URL:		http://dalibo.github.com/pgbadger/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

%description
pgBadger is a PostgreSQL log analyzer build for speed with fully 
detailed reports from your PostgreSQL log file. It's a single and small 
Perl script that aims to replace and outperform the old php script 
pgFouine.

pgBadger is written in pure Perl language. It uses a javascript library 
to draw graphs so that you don't need additional Perl modules or any 
other package to install. Furthermore, this library gives us more 
features such as zooming.

pgBadger is able to autodetect your log file format (syslog, stderr or 
csvlog). It is designed to parse huge log files as well as gzip 
compressed file. 

%prep
%setup -q 
%patch0 -p0

%{__perl} Makefile.PL INSTALLDIRS=vendor

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}
%perl_vendorarch/auto/pgBadger/.packlist
%{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Oct 16 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.2-1
- Update to 6.2

* Thu Oct 16 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.1-1
- Update to 6.1

* Wed Aug 27 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Tue May 6 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 5.1-1
- Update to 5.1                          

* Thu Feb 13 2014 - Devrim GÜNDÜZ <devrim@gunduz.org> 5.0-1
- Update to 5.0, per changes described at
  http://www.postgresql.org/message-id/2c9e60c9f80fe68276178abe45311d09@dalibo.com

* Thu Nov 08 2013 - Jeff Frost <jeff@pgexperts.com> 4.1-1
- Update to 4.1

* Thu Oct 31 2013 - Jeff Frost <jeff@pgexperts.com> 4.0-1
- Update to 4.0

* Mon Sep 23 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 3.6-1
- Update to 3.6

* Mon Sep 16 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 3.5-1
- Update to 3.5

* Thu Jun 20 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.4-1
- Update to 3.4

* Thu Apr 11 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.2-1
- Update to 3.2
- Add a patch so that pgbadger works with Perl 5.8. Per #98.

* Tue Feb 26 2013 - Devrim GUNDUZ <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Mon Jan 21 2013 - Devrim GUNDUZ <devrim@gunduz.org> 2.3-1
- Update to 2.3
- Update download URL.

* Wed Nov 14 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Thu Nov 1 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Thu Sep 26 2012 - Devrim GUNDUZ <devrim@gunduz.org> 2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
