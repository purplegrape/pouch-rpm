%global             debug_package   %{nil}
%global             _dwz_low_mem_die_limit 0
%global             __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:               pouch
Version:            1.0.0
Release:            3%{?dist}
Summary:            An Efficient Container Engine

License:            apache 2.0
URL:                https://github.com/alibaba/pouch

Source0:            %{name}-%{version}.tar.gz
Source1:            containerd-1.0.3.linux-amd64.tar.gz

Source11:           pouchd.sysconfig
Source12:           pouchd.service
Source13:           pouchd-lxcfs.service

BuildRequires:      golang >= 1.9.0
BuildRequires:      systemd
BuildRequires:      golang-github-cpuguy83-go-md2man

Requires:           lxcfs = 2.0.8
Requires:           containernetworking-plugins >= 0.6
Requires:           runc >= 1.0
Requires:           systemd
Requires:           bash-completion

%description
Pouch is an open-source project created by Alibaba Group to promote the container technology movement.
Pouch can pack, deliver and run any application. It provides the enviroment for applications with strong isolation in quite lightweight way. 
Pouch not only splits the application itself from the underlying environment, but also has ability to remain the good experience of operation.

%prep
%setup -q -a 1

%build
export GOPATH=%{_builddir}/%{buildsubdir}/_output
mkdir -p _output/src/github.com/alibaba
ln -sf %{_builddir}/%{buildsubdir}  _output/src/github.com/alibaba/pouch
cd _output/src/github.com/alibaba/pouch
make %{?_smp_mflags}

cd docs/commandline
for i in `ls pouch*.md`;do
    output=${i%.md}
    go-md2man -in $i -out $output.1
    gzip *.1
done

%install
rm -rf $RPM_BUILD_ROOT

%{__mkdir} -p $RPM_BUILD_ROOT%{_sharedstatedir}/pouch
%{__mkdir} -p $RPM_BUILD_ROOT%{_sharedstatedir}/pouch-lxcfs
%{__mkdir} -p $RPM_BUILD_ROOT%{_mandir}/man1/

%{__install} -D -m 755 bin/pouch                $RPM_BUILD_ROOT%{_bindir}/pouch
%{__install} -D -m 755 bin/pouchd               $RPM_BUILD_ROOT%{_bindir}/pouchd
%{__install} -D -m 755 bin/containerd           $RPM_BUILD_ROOT%{_bindir}/containerd
%{__install} -D -m 755 bin/containerd-release   $RPM_BUILD_ROOT%{_bindir}/containerd-release
%{__install} -D -m 755 bin/containerd-shim      $RPM_BUILD_ROOT%{_bindir}/containerd-shim
%{__install} -D -m 755 bin/containerd-stress    $RPM_BUILD_ROOT%{_bindir}/containerd-stress

%{__install} -D -m 644 contrib/completion/bash/pouch $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/pouch.bash-completion

%{__install} -D -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/pouchd
%{__install} -D -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/pouchd.service
%{__install} -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/lxcfs.service

mv docs/commandline/*.gz $RPM_BUILD_ROOT%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "pouch" user
getent group pouch  >/dev/null || groupadd -r pouch
getent passwd pouch >/dev/null || useradd -r -g pouch -s /sbin/nologin -d /var/lib/pouch pouch
exit 0

%post
%systemd_post pouchd.service

%preun
%systemd_preun pouchd.service

%postun
%systemd_postun_with_restart pouchd.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/pouchd
%{_sysconfdir}/bash_completion.d/pouch.bash-completion
%{_sysconfdir}/systemd/system/lxcfs.service
%{_unitdir}/pouchd.service
%dir %{_sharedstatedir}/pouch
%dir %{_sharedstatedir}/pouch-lxcfs
%{_mandir}/man1/*

%changelog
* Thu Oct 25 2018 Purple Grape <purplegrape4@gmail.com>
- update to 1.0.0
