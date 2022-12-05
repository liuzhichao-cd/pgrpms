%global sname	jsquery

Summary:	PostgreSQL json query language with GIN indexing support
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.1
Release:	3%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/ver_%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}/

BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
JsQuery – is a language to query jsonb data type, introduced in
PostgreSQL release 9.4.

It's primary goal is to provide an additional functionality to jsonb
(currently missing in PostgreSQL), such as a simple and effective way to
search in nested objects and arrays, more comparison operators with
indexes support. We hope, that jsquery will be eventually a part of
PostgreSQL.

Jsquery is released as jsquery data type (similar to tsquery) and @@
match operator for jsonb.

%package devel
Summary:	JsQuery development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes the development headers for the jsquery extension.

%prep
%setup -q -n %{sname}-ver_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/include/server
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%ifarch ppc64 ppc64le
 %else
 %if %{pgmajorversion} >= 11 && %{pgmajorversion} < 90
  %if 0%{?rhel} && 0%{?rhel} <= 6
  %else
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %endif
 %endif
%endif

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/jsquery*.h

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue May 5 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.1.1-2
- Fix -devel package dependency, per report from Justin.

* Fri Sep 6 2019 - Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Rebuild against PostgreSQL 11.0

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
