%undefine _package_note_file

# These are macros to be used with find_lang and other stuff
%global packageversion 160
%global pgpackageversion 16
%global prevmajorversion 15
%global sname postgresql
%global pgbaseinstdir	/usr/pgsql-%{pgmajorversion}

%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}

# Macros that define the configure parameters:
%{!?kerbdir:%global kerbdir "/usr"}

%if 0%{?suse_version} >= 1315
%{!?enabletaptests:%global enabletaptests 0}
%else
%{!?enabletaptests:%global enabletaptests 1}
%endif

%{!?icu:%global icu 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}

%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?plpython3:%global plpython3 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?runselftest:%global runselftest 0}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}

%ifarch ppc64 ppc64le s390 s390x armv7hl
%{!?sdt:%global sdt 0}
%else
 %{!?sdt:%global sdt 1}
%endif

%{!?llvm:%global llvm 1}

%{!?selinux:%global selinux 1}

%if 0%{?fedora} > 30
%global _hardened_build 1
%endif

#Filter out some Perl "dependencies"
%global __requires_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)
%global __provides_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)

Summary:	PostgreSQL client programs and libraries
Name:		%{sname}%{pgmajorversion}
Version:	16.3
%if 0%{?suse_version} >= 1315
# SuSE upstream packages have release numbers like 150200.5.19.1
# which overrides our packages. Increase our release number on SuSE.
Release:	420001PGDG%{?dist}
%else
Release:	1PGDG%{?dist}
%endif
License:	PostgreSQL
Url:		https://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source4:	%{sname}-%{pgmajorversion}-Makefile.regress
Source5:	%{sname}-%{pgmajorversion}-pg_config.h
Source6:	%{sname}-%{pgmajorversion}-README-systemd.rpm-dist
Source7:	%{sname}-%{pgmajorversion}-ecpg_config.h
Source9:	%{sname}-%{pgmajorversion}-libs.conf
Source12:	https://www.postgresql.org/files/documentation/pdf/%{pgpackageversion}/%{sname}-%{pgpackageversion}-A4.pdf
%if 0%{?suse_version}
Source14:	%{sname}-%{pgmajorversion}.pam.suse
%else
Source14:	%{sname}-%{pgmajorversion}.pam
%endif
Source17:	%{sname}-%{pgmajorversion}-setup
Source10:	%{sname}-%{pgmajorversion}-check-db-dir
Source18:	%{sname}-%{pgmajorversion}.service
Source19:	%{sname}-%{pgmajorversion}-tmpfiles.d

Patch1:		%{sname}-%{pgmajorversion}-rpm-pgsql.patch
Patch3:		%{sname}-%{pgmajorversion}-conf.patch
Patch5:		%{sname}-%{pgmajorversion}-var-run-socket.patch
Patch6:		%{sname}-%{pgmajorversion}-perl-rpath.patch

BuildRequires:	perl glibc-devel bison flex >= 2.5.31
BuildRequires:	gcc-c++
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	readline-devel zlib-devel >= 1.0.4 pgdg-srpm-macros

# lz4 dependency
%if 0%{?suse_version} >= 1315
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4
%endif

# zstd dependency
%if 0%{?suse_version} >= 1499
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif

# This dependency is needed for Source 16:
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	perl-generators
%endif

Requires:	/sbin/ldconfig

%if %icu
BuildRequires:	libicu-devel
Requires:	libicu
%endif

%if 0%{?rhel} && 0%{?rhel} >= 8
# Packages come from Appstream:
BuildRequires:	llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?fedora}
BuildRequires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %ldap
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %plperl
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 8
BuildRequires:	perl-ExtUtils-Embed
%endif
%endif

BuildRequires:	python3-devel

%if %pltcl
BuildRequires:	tcl-devel
%endif

%if %sdt
BuildRequires:	systemtap-sdt-devel
%endif

%if %selinux
# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.0.93
# SLES: SLES 15 does not have selinux-policy package. Use
# it only on SLES 12:
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	selinux-policy >= 3.9.13
%endif
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
%endif
%endif

%if %ssl
%if 0%{?suse_version} >= 1315
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif
%endif

%if %uuid
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	uuid-devel
%endif
%else
BuildRequires:	libuuid-devel
%endif
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Provides:	%{sname} >= %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system. These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection. The PostgreSQL server can be found in the
postgresql%{pgmajorversion}-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql%{pgmajorversion}-server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Provides:	postgresql-libs = %{pgmajorversion} libpq5 >= 10.0

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires:	openssl
%else
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	libopenssl1_0_0
%else
%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.0.2k
%endif
%endif
%endif

%description libs
The postgresql%{pgmajorversion}-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):	/usr/sbin/useradd /usr/sbin/groupadd
Requires:	util-linux
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc
# pre/post stuff needs systemd too

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd
%endif
%else
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Provides:	postgresql-server >= %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql%{pgmajorversion}-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.

%package docs
Summary:	Extra documentation for PostgreSQL
Provides:	postgresql-docs >= %{version}-%{release}

%description docs
The postgresql%{pgmajorversion}-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Provides:	postgresql-contrib >= %{version}-%{release}

%description contrib
The postgresql%{pgmajorversion}-contrib package contains various extension modules that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
%if %llvm
%if 0%{?rhel} && 0%{?rhel} >= 8
# Packages come from Appstream:
Requires:	llvm-devel >= 8.0.1 clang-devel >= 8.0.1
%endif
%if 0%{?fedora}
Requires:	llvm-devel >= 5.0 clang-devel >= 5.0
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
Requires:	llvm6-devel clang6-devel
%endif
%if 0%{?suse_version} >= 1500
Requires:	llvm15-devel clang15-devel
%endif
%endif
%if %icu
Requires:	libicu-devel
%endif

%if %enabletaptests
%if 0%{?suse_version} && 0%{?suse_version} >= 1315
Requires:	perl-IPC-Run
BuildRequires:	perl-IPC-Run
%endif
%if 0%{?rhel}
Requires:	perl-Test-Simple
BuildRequires:	perl-Test-Simple perl-IPC-Run perl-Time-HiRes
%endif
%if 0%{?fedora}
Requires:	perl-IPC-Run
BuildRequires:	perl-Test-Simple perl-IPC-Run perl-Time-HiRes
%endif
%endif

Provides:	postgresql-devel >= %{version}-%{release}
Obsoletes:	libpq-devel <= 42.0

%description devel
The postgresql%{pgmajorversion}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a PostgreSQL server.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1315
Requires:	llvm
%endif
%if 0%{?suse_version} >= 1500
Requires:	libLLVM15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

Provides:	postgresql-llvmjit >= %{version}-%{release}

%description llvmjit
The postgresql%{pgmajorversion}-llvmjit package contains support for
just-in-time compiling parts of PostgreSQL queries. Using LLVM it
compiles e.g. expressions and tuple deforming into native code, with the
goal of accelerating analytics queries.
%endif

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Provides:	postgresql-plperl >= %{version}-%{release}

%description plperl
The postgresql%{pgmajorversion}-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython3
%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Provides:	postgresql-plpython3 >= %{version}-%{release}
%if 0%{?suse_version} >= 1315
Requires:	python3-base
%else
Requires:	python3-libs
%endif

%description plpython3
The postgresql%{pgmajorversion}-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	tcl
Provides:	postgresql-pltcl >= %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	postgresql-test >= %{version}-%{release}

%description test
The postgresql%{pgmajorversion}-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%prep
%setup -q -n %{sname}-%{version}

%patch -P 1 -p0
%patch -P 3 -p0
%patch -P 5 -p0
%patch -P 6 -p0

%{__cp} -p %{SOURCE12} .

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "postgresql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="${CFLAGS:-%optflags}"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%if 0%{?rhel}
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
%endif

export CFLAGS

%if 0%{?fedora} >= 37 || 0%{?rhel} >= 8
export CLANG=%{_bindir}/clang LLVM_CONFIG=%{_bindir}/llvm-config-64
%endif
%if 0%{?suse_version} >= 1315
export CLANG=%{_bindir}/clang LLVM_CONFIG=%{_bindir}/llvm-config
%endif

# These configure options must match main build
./configure --enable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
	--libdir=%{pgbaseinstdir}/lib \
	--with-lz4 \
%if 0%{?rhel} || 0%{?suse_version} >= 1499 || 0%{?fedora}
	--with-zstd \
%endif
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %enabletaptests
	--enable-tap-tests \
%endif
%if %icu
	--with-icu \
%endif
%if %llvm
	--with-llvm \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython3
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %sdt
	--enable-dtrace \
%endif
%if %uuid
	--with-uuid=e2fs \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux \
%endif
	--with-systemd \
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{pgbaseinstdir}/doc \
	--htmldir=%{pgbaseinstdir}/doc/html

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%{__make} %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
%{__rm} -f src/tutorial/GNUmakefile

MAKELEVEL=0 %{__make} %{?_smp_mflags} all
%{__make} %{?_smp_mflags} -C contrib all
%if %uuid
%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
%endif


# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path. When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.

run_testsuite()
{
	%{__make} -C "$1" MAX_CONNECTIONS=5 check && return 0

	test_failure=1

	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

%if %runselftest
	run_testsuite "src/test/regress"
	%{__make} clean -C "src/test/regress"
	run_testsuite "src/pl"
%if %plpython3
	run_testsuite "src/pl/plpython"
%endif
	run_testsuite "contrib"
%endif

%if %test
	pushd src/test/regress
	%{__make} all
	popd
%endif

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

	# Install PL/Python3
%if %plpython3
	pushd src/pl/plpython
	%{__make} DESTDIR=%{buildroot} install
	popd
%endif

%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/extensions/
%{__make} -C contrib DESTDIR=%{buildroot} install
%if %uuid
%{__make} -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/pg_config.h
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h
		;;
	*)
	;;
esac

# This is only for systemd supported distros:
# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PGENGINE=.*$|PGENGINE=%{pgbaseinstdir}/bin|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	<%{SOURCE17} >postgresql-%{pgmajorversion}-setup
%{__install} -m 755 postgresql-%{pgmajorversion}-setup %{buildroot}%{pgbaseinstdir}/bin/postgresql-%{pgmajorversion}-setup
# Create a symlink of the setup script under $PATH
%{__mkdir} -p %{buildroot}%{_bindir}
%{__ln_s} ../../../../../../../../../../../../../../%{pgbaseinstdir}/bin/postgresql-%{pgmajorversion}-setup %{buildroot}%{_bindir}/

# prep the startup check script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	-e 's|^PGDOCDIR=.*$|PGDOCDIR=%{_pkgdocdir}|' \
	<%{SOURCE10} >%{sname}-%{pgmajorversion}-check-db-dir
touch -r %{SOURCE10} %{sname}-%{pgmajorversion}-check-db-dir
%{__install} -m 755 %{sname}-%{pgmajorversion}-check-db-dir %{buildroot}%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

%if %pam
%{__install} -d %{buildroot}/etc/pam.d
%{__install} -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/%{sname}
%endif

# Create the directory for sockets.
%{__install} -d -m 755 %{buildroot}/%{_rundir}/%{sname}
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE19} %{buildroot}/%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 %{buildroot}/var/lib/pgsql/%{pgmajorversion}/data

# backups of data go here...
%{__install} -d -m 700 %{buildroot}/var/lib/pgsql/%{pgmajorversion}/backups

# Create the multiple PostgreSQL version startup directory
%{__install} -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{pgmajorversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %{buildroot}%{pgbaseinstdir}/share/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{pgbaseinstdir}/share/

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness. We replace the original
	# Makefiles, however.
	%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/lib/test
	%{__cp} -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/refint.so
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/autoinc.so
	# pg_regress binary should be only in one subpackage,
	# there will be a symlink from -test to -devel
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/pg_regress
	%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/lib/pgsql/test/regress/
	%{__ln_s} -f ../../pgxs/src/test/regress/pg_regress %{buildroot}%{pgbaseinstdir}/lib/test/regress/pg_regress
	pushd %{buildroot}%{pgbaseinstdir}/lib/test/regress
	strip *.so
	%{__rm} -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	%{__cp} %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

%if %plpython3
# Quick hack:
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpython2u*
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpythonu-*
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*_plpythonu.control
%endif

# Fix some more documentation
# gzip doc/internals.ps
%{__cp} %{SOURCE6} README.rpm-dist
%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/doc/html
%{__mv} doc/src/sgml/html doc
%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/man/
%{__mv} doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7 %{buildroot}%{pgbaseinstdir}/share/man/
%{__rm} -rf %{buildroot}%{_docdir}/pgsql

# These file(s) should not be packaged:
%{__rm} %{buildroot}%{pgbaseinstdir}/lib/libpgfeutils.a

# initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython.lst
%{__cp} /dev/null pg_plpython3.lst
%{__cp} /dev/null pg_checksums.lst

%if %nls
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_amcheck-%{pgmajorversion}
%find_lang pg_archivecleanup-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_checksums-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetwal-%{pgmajorversion}
%find_lang pg_rewind-%{pgmajorversion}
%find_lang pg_test_fsync-%{pgmajorversion}
%find_lang pg_test_timing-%{pgmajorversion}
%find_lang pg_upgrade-%{pgmajorversion}
%find_lang pg_verifybackup-%{pgmajorversion}
%find_lang pg_waldump-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%if %plperl
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgmajorversion}
%if %plpython3
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang >> pg_plpython3.lst
%endif

%if %pltcl
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}

cat pg_amcheck-%{pgmajorversion}.lang > pg_contrib.lst
cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst
cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang > pg_devel.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetwal-%{pgmajorversion}.lang pg_checksums-%{pgmajorversion}.lang pg_verifybackup-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang pg_test_timing-%{pgmajorversion}.lang pg_test_fsync-%{pgmajorversion}.lang pg_archivecleanup-%{pgmajorversion}.lang pg_waldump-%{pgmajorversion}.lang pg_rewind-%{pgmajorversion}.lang pg_upgrade-%{pgmajorversion}.lang > pg_server.lst
%endif

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre postgresql-%{pgpackageversion}.service
   %endif
   %else
   %systemd_post %{sname}-%{pgpackageversion}.service
   %endif
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/%{pgmajorversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" > /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

%preun server
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%postun server
/sbin/ldconfig
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install %{_bindir}/psql pgsql-psql %{pgbaseinstdir}/bin/psql %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/clusterdb pgsql-clusterdb %{pgbaseinstdir}/bin/clusterdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createdb pgsql-createdb %{pgbaseinstdir}/bin/createdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createuser pgsql-createuser %{pgbaseinstdir}/bin/createuser %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropdb pgsql-dropdb %{pgbaseinstdir}/bin/dropdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropuser pgsql-dropuser %{pgbaseinstdir}/bin/dropuser %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_basebackup pgsql-pg_basebackup %{pgbaseinstdir}/bin/pg_basebackup %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dump pgsql-pg_dump %{pgbaseinstdir}/bin/pg_dump %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dumpall pgsql-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_restore pgsql-pg_restore %{pgbaseinstdir}/bin/pg_restore %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/reindexdb pgsql-reindexdb %{pgbaseinstdir}/bin/reindexdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/vacuumdb pgsql-vacuumdb %{pgbaseinstdir}/bin/vacuumdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/clusterdb.1 pgsql-clusterdbman %{pgbaseinstdir}/share/man/man1/clusterdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createdb.1 pgsql-createdbman %{pgbaseinstdir}/share/man/man1/createdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createuser.1 pgsql-createuserman %{pgbaseinstdir}/share/man/man1/createuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropdb.1 pgsql-dropdbman %{pgbaseinstdir}/share/man/man1/dropdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropuser.1 pgsql-dropuserman %{pgbaseinstdir}/share/man/man1/dropuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_basebackup.1 pgsql-pg_basebackupman %{pgbaseinstdir}/share/man/man1/pg_basebackup.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dump.1 pgsql-pg_dumpman %{pgbaseinstdir}/share/man/man1/pg_dump.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dumpall.1 pgsql-pg_dumpallman %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_restore.1 pgsql-pg_restoreman %{pgbaseinstdir}/share/man/man1/pg_restore.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/psql.1 pgsql-psqlman %{pgbaseinstdir}/share/man/man1/psql.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/reindexdb.1 pgsql-reindexdbman %{pgbaseinstdir}/share/man/man1/reindexdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/vacuumdb.1 pgsql-vacuumdbman %{pgbaseinstdir}/share/man/man1/vacuumdb.1 %{packageversion}0

%post libs
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/%{sname}-pgdg-libs.conf pgsql-ld-conf %{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf %{packageversion}0
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgsql-psql		%{pgbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgsql-clusterdb	%{pgbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgsql-clusterdbman	%{pgbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createdb		%{pgbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgsql-createdbman	%{pgbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createuser	%{pgbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgsql-createuserman	%{pgbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgsql-dropdb		%{pgbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgsql-dropdbman	%{pgbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgsql-dropuser		%{pgbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgsql-dropuserman	%{pgbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackup	%{pgbaseinstdir}/bin/pg_basebackup
	%{_sbindir}/update-alternatives --remove pgsql-pg_dump		%{pgbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpall	%{pgbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpallman	%{pgbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackupman	%{pgbaseinstdir}/share/man/man1/pg_basebackup.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpman	%{pgbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_restore	%{pgbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgsql-pg_restoreman	%{pgbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgsql-psqlman		%{pgbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgsql-reindexdb	%{pgbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgsql-reindexdbman	%{pgbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdb		%{pgbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdbman	%{pgbaseinstdir}/share/man/man1/vacuumdb.1
  fi

%postun libs
if [ "$1" -eq 0 ]
  then
	%{_sbindir}/update-alternatives --remove pgsql-ld-conf		%{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf
	/sbin/ldconfig
fi

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%if %llvm
# Install bitcode directory along with the main package,
# so that extensions can use this dir.
%dir %{pgbaseinstdir}/lib/bitcode
%endif
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_receivewal
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_waldump
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/errcodes.txt
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pgbench.1
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_isready.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib -f pg_contrib.lst
%defattr(-,root,root)
%doc %{pgbaseinstdir}/doc/extension/*.example
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/amcheck.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/basebackup_to_shell.so
%{pgbaseinstdir}/lib/basic_archive.so
%{pgbaseinstdir}/lib/bloom.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%if %plperl
%{pgbaseinstdir}/lib/hstore_plperl.so
%{pgbaseinstdir}/lib/jsonb_plperl.so
%{pgbaseinstdir}/share/extension/jsonb_plperl*.sql
%{pgbaseinstdir}/share/extension/jsonb_plperl*.control
%endif
%if %plpython3
%{pgbaseinstdir}/lib/hstore_plpython3.so
%{pgbaseinstdir}/lib/jsonb_plpython3.so
%{pgbaseinstdir}/lib/ltree_plpython3.so
%endif
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/old_snapshot.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_prewarm.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pg_surgery.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/pg_visibility.so
%{pgbaseinstdir}/lib/pg_walinspect.so
%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%if %ssl
%{pgbaseinstdir}/lib/sslinfo.so
%endif
%if %selinux
%{pgbaseinstdir}/lib/sepgsql.so
%{pgbaseinstdir}/share/contrib/sepgsql.sql
%endif
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/test_decoding.so
%{pgbaseinstdir}/lib/tsm_system_rows.so
%{pgbaseinstdir}/lib/tsm_system_time.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/extension/adminpack*
%{pgbaseinstdir}/share/extension/amcheck*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/bloom*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore.control
%{pgbaseinstdir}/share/extension/hstore--*.sql
%if %plperl
%{pgbaseinstdir}/share/extension/hstore_plperl*
%endif
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree.control
%{pgbaseinstdir}/share/extension/ltree--*.sql
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/old_snapshot*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_prewarm*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_surgery*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pg_visibility*
%{pgbaseinstdir}/share/extension/pg_walinspect*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%if %ssl
%{pgbaseinstdir}/share/extension/sslinfo*
%endif
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/tsm_system_rows*
%{pgbaseinstdir}/share/extension/tsm_system_time*
%{pgbaseinstdir}/share/extension/unaccent*
%if %uuid
%{pgbaseinstdir}/share/extension/uuid-ossp*
%endif
%if %xml
%{pgbaseinstdir}/share/extension/xml2*
%endif
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pg_amcheck
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/share/man/man1/pg_amcheck.1
%{pgbaseinstdir}/share/man/man1/oid2name.1
%{pgbaseinstdir}/share/man/man1/pg_recvlogical.1
%{pgbaseinstdir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-setup
%{_bindir}/%{sname}-%{pgmajorversion}-setup
%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir
%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%if %pam
%config(noreplace) /etc/pam.d/%{sname}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_checksums
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetwal
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_verifybackup
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/share/fix-CVE-2024-4317.sql
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.1
%{pgbaseinstdir}/share/man/man1/pg_checksums.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetwal.*
%{pgbaseinstdir}/share/man/man1/pg_receivewal.*
%{pgbaseinstdir}/share/man/man1/pg_rewind.1
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.1
%{pgbaseinstdir}/share/man/man1/pg_test_timing.1
%{pgbaseinstdir}/share/man/man1/pg_upgrade.1
%{pgbaseinstdir}/share/man/man1/pg_verifybackup.*
%{pgbaseinstdir}/share/man/man1/pg_waldump.1
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/system_constraints.sql
%{pgbaseinstdir}/share/system_functions.sql
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/pgoutput.so
%{pgbaseinstdir}/lib/plpgsql.so
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}/backups
%attr(755,postgres,postgres) %dir %{_rundir}/%{sname}
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/libpgcommon_shlib.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgport_shlib.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%if %llvm
%files llvmjit
%defattr(-,root,root)
%{pgbaseinstdir}/lib/bitcode/*
%{pgbaseinstdir}/lib/llvmjit.so
%{pgbaseinstdir}/lib/llvmjit_types.bc
%endif

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/bool_plperl.so
%{pgbaseinstdir}/lib/plperl.so
%{pgbaseinstdir}/share/extension/plperl*
%{pgbaseinstdir}/share/extension/bool_plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/share/extension/pltcl*
%endif

%if %plpython3
%files plpython3 -f pg_plpython3.lst
%{pgbaseinstdir}/share/extension/plpython3*
%{pgbaseinstdir}/lib/plpython3.so
%{pgbaseinstdir}/share/extension/*_plpython3u*
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Tue May 7 2024 Devrim Gunduz <devrim@gunduz.org> - 16.3-1PGDG
- Update to 16.3, per changes described at:
  https://www.postgresql.org/docs/release/16.3/

* Tue Feb 6 2024 Devrim Gunduz <devrim@gunduz.org> - 16.2-1PGDG
- Update to 16.2, per changes described at:
  https://www.postgresql.org/docs/release/16.2/

* Mon Jan 8 2024 Devrim Gunduz <devrim@gunduz.org> - 16.1-8PGDG
- SuSE upstream packages have release numbers like 150200.5.19.1
  which overrides our packages. Increase our release number on SuSE.

* Fri Jan 5 2024 Devrim Gunduz <devrim@gunduz.org> - 16.1-7PGDG
- Fix a couple of BR for SLES 15. Per report from Muralikrishna Bandaru.

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 16.1-6PGDG
- Update legacy path /var/run to /run. Also use macros in the spec file for
  that.

* Tue Nov 21 2023 Devrim Gündüz <devrim@gunduz.org> - 16.1-5PGDG
- Rebuild on RHEL 9.3 / aarch64 against new LLVM

* Mon Nov 20 2023 Devrim Gündüz <devrim@gunduz.org> - 16.1-4PGDG
- Rebuild against new LLVM on RHEL 8.9

* Sun Nov 19 2023 Devrim Gunduz <devrim@gunduz.org> - 16.1-3PGDG
- Enable LLVM on all supported platforms.

* Mon Nov 13 2023 Devrim Gunduz <devrim@gunduz.org> - 16.1-2PGDG
- Enable plpython subpackage, which is an oversight of commit
  2e6573c653 . Per report from Laurent Parodi. Fixes
  https://redmine.postgresql.org/issues/7903

* Tue Nov 7 2023 Devrim Gunduz <devrim@gunduz.org> - 16.1-1PGDG
- Update to 16.1, per changes described at:
  https://www.postgresql.org/docs/release/16.1/

* Fri Oct 27 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-4PGDG
- Remove references to RHEL 7. While passing, export CLANG and LLVM
  on all distros. Per report from Greg Hennessy:
  https://www.postgresql.org/message-id/CA%2BmZaON9nDxWrg%3DABBczU3DuYwQ3Q02atsY%2BXhb0ogAgHzmYVg%40mail.gmail.com

* Wed Oct 18 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-3PGDG
- Add temp patches to support newer LLVM until 16.1 is out.

* Tue Sep 19 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-2PGDG
- Re-add plpython3 (was plpython) build macro for the users who don't
  want to build with PL/Python (make it consistent with other PLs)

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-1PGDG
- Update to v16.0 Gold!

* Tue Aug 29 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-rc1-1PGDG
- Update to v16 RC 1
- Remove LLVM dependency in the main package on SLES 15. Per bug report
  from Muralikrishna Bandaru.

* Tue Aug 8 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-beta3-1
- Update to v16 beta3

* Thu Jun 29 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-beta2-1
- Update to v16 beta2

* Sun Jun 4 2023 Devrim Gündüz <devrim@gunduz.org> - 16.0-beta1-2
- Rebuild against LLVM 15 on SLES 15

* Tue May 23 2023 Devrim Gunduz <devrim@gunduz.org> - 16.0-beta1-1
- Update to v16 beta1
- Remove a few configure parameters: plpython3 and systemd_enabled are no longer
  needed, as they are supported on all distros. Also remove %%disablepgfts macro.

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 16-alpha_20230424_PGDG.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Tue Feb 7 2023 Devrim Gündüz <devrim@gunduz.org> - 16-alpha_20230208_PGDG.1
- Enable TAP tests on all RHEL versions, per report from Bill Smith.
  Commit 4f08cb8d41b8 is now obsolete, it seems.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 16-alpha_20221205_PGDG.1
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> - 16.0-alpha
- Initial cut for PostgreSQL 16.

