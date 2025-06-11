Name:           libosmo-netif
Version:        1.6.0
Release:        1.dcbw%{?dist}
Summary:        Osmocom network interface library
License:        GPL-2.0-or-later

URL:            https://osmocom.org/projects/libosmo-netif/wiki

BuildRequires:  git gcc autoconf automake libtool doxygen
BuildRequires:  lksctp-tools-devel libpcap-devel
BuildRequires:  libosmocore-devel >= 1.10.0

Source0: %{name}-%{version}.tar.bz2

%description
C-language library that form the basis of various higher-layer
cellular communications protocol implementation. It implements
stream server and clients for TCP, UDP, IPA as well as the
non-standard/proprietary OSMUX protocol.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}.


%prep
%autosetup -p1

%build
%global optflags %(echo %optflags | sed 's|-Wp,-D_GLIBCXX_ASSERTIONS||g')
echo "%{version}" >.tarball-version
autoreconf -fi
%configure --enable-shared \
           --disable-static

# Fix unused direct shlib dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} \;
sed -i -e 's|UNKNOWN|%{version}|g' %{buildroot}/%{_libdir}/pkgconfig/*.pc


%check
make check


%ldconfig_scriptlets


%files
%doc README.md
%doc %{_docdir}/%{name}
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/osmocom/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Jun  8 2025 Dan Williams <dan@ioncontrol.co> - 1.6.0
- Update to 1.6.0

* Sun Aug 26 2018 Cristian Balint <cristian.balint@gmail.com>
- github update releases
