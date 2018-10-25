%global             debug_package   %{nil}

Name:               lxcfs
Version:            2.0.8
Release:            1%{?dist}
Summary:            FUSE filesystem for LXC

License:            ASL 2.0
URL:                https://linuxcontainers.org

Source0:            https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Patch0:             lxcfs-2.0.5-Fix-systemd-unit-directory.patch
Patch1:             lxcfs-2.0.5-Fix-fusermount-path.patch

BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      help2man
BuildRequires:      libtool
BuildRequires:      pam-devel
BuildRequires:      pkgconfig
BuildRequires:      fuse-devel
BuildRequires:      systemd-units

Requires:           systemd
Requires:           fuse
Requires:           fuse-libs

AutoProv:           no

%description
LXCFS is a simple userspace filesystem designed to work
around some current limitations of the Linux kernel.

Specifically, it's providing two main things

- A set of files which can be bind-mounted over their
  /proc originals to provide CGroup-aware values.
- A cgroupfs-like tree which is container aware. The
  code is pretty simple, written in C using libfuse
  and glib.

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf --force --install
%configure --with-init-script=systemd
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/lxc
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_unitdir}/%{name}.service
%dir %{_sharedstatedir}/%{name}
%doc AUTHORS
%license COPYING

%exclude %{_libdir}/lxcfs/liblxcfs.la
%exclude /%{_lib}/security/pam_cgfs.so
