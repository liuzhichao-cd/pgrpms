%global _vpath_builddir .
%global pgroutingmajorversion 3.1
%global sname	pgrouting

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.4
Release:	2%{dist}
License:	GPLv2+
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://pgrouting.org/
BuildRequires:	gcc-c++
%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	cmake3
# EPEL:
BuildRequires:	boost169-devel
%else
BuildRequires:	cmake => 3.2.0
BuildRequires:	boost-devel >= 1.53
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	gmp-devel
Requires:	postgis >= 2.3

Requires:	postgresql%{pgmajorversion}

%description
pgRouting extends the PostGIS / PostgreSQL geospatial database to
provide geospatial routing functionality.

Advantages of the database routing approach are:

- Data and attributes can be modified by many clients, like QGIS and
uDig through JDBC, ODBC, or directly using Pl/pgSQL. The clients can
either be PCs or mobile devices)
- Data changes can be reflected instantaneously through the routing
engine. There is no need for precalculation.
- The “cost” parameter can be dynamically calculated through SQL and its
value can come from multiple fields or tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake .. \
%else
%cmake3 .. \
%endif
%if 0%{?rhel} && 0%{?rhel} == 7
	-DBOOST_ROOT=%{_includedir}/boost169 \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_BIN=%{pginstdir}/bin \
	-DCMAKE_BUILD_TYPE=Release \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

%clean
%{__rm} -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md BOOST_LICENSE_1_0.txt
%attr(755,root,root) %{pginstdir}/lib/libpgrouting-%{pgroutingmajorversion}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 25 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4, to fix RHEL 7 builds.

* Tue Jan 26 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3
- Update License

* Sun Dec 20 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.2-1
- Update to 3.1.2

* Thu Oct 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-3
- Build fixes for Fedora 33

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-2
- Require PostGIS >= 2.3, per Vicky.

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Initial packaging of pgRouting 3.1
