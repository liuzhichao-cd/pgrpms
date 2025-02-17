%global pname vector
%global sname pgvector

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.7.0
Release:	2PGDG%{?dist}
Summary:	Open-source vector similarity search for Postgres
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

# To be removed when upstream releases a version with this patch:
# https://github.com/pgvector/pgvector/pull/311
Patch0:		pgvector-0.6.2-fixillegalinstructionrror.patch

%if 0%{?rhel} == 8
# RHEL 8 only patch for 0.7.0. Upstream issue:
# https://github.com/pgvector/pgvector/issues/538
Patch1:		pgvector-0.7.0-rhel8-gcc8.patch
%endif

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Open-source vector similarity search for Postgres. Supports L2 distance,
inner product, and cosine distance

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgvector
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for pgvector
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0
%if 0%{?rhel} == 8
%patch -P 1 -p1
%endif

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

#Remove header file, we don't need it right now:
%{__rm} %{buildroot}%{pginstdir}/include/server/extension/%{pname}/%{pname}.h

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension//%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%dir %{pginstdir}/include/server/extension/vector/
%{pginstdir}/include/server/extension/vector/*.h

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*.bc
   %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Thu May 2 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-2PGDG
- Add a patch from upstream to fix extension instsallation on RHEL 8.
  https://github.com/pgvector/pgvector/issues/538

* Tue Apr 30 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1PGDG
- Update to 0.7.0

* Wed Apr 3 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-2PGDG
  Add a patch to solve "illegal instruction error". This patch will be removed
  in 0.7.0 per: https://github.com/pgvector/pgvector/pull/311

* Wed Mar 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Update to 0.6.2

* Mon Mar 4 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-1PGDG
- Update to 0.6.1

* Mon Jan 29 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1PGDG
- Update to 0.6.0

* Wed Oct 11 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Update to 0.5.1

* Thu Aug 31 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1PGDG
- Update to 0.5.0
- Add PGDG branding

* Tue Jun 13 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.4-1
- Update to 0.4.4

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 0.4.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.2-1
- Update to 0.4.2

* Thu Mar 30 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Initial packaging for PostgreSQL YUM repository.

