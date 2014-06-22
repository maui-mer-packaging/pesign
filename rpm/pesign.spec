# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       pesign

# >> macros
# << macros

Summary:    Signing utility for UEFI binaries
Version:    0.108
Release:    1
Group:      Development/System
License:    GPLv2
ExclusiveArch:  i686 x86_64 ia64
URL:        https://github.com/vathpela/pesign
Source0:    %{name}-%{version}.tar.xz
Source100:  pesign.yaml
Patch0:     0001-Don-t-set-SO_PASSCRED.patch
Requires:   nspr nss nss-util popt rpm coolkey opensc
Requires(pre): shadow-utils
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  nspr nss nss-util popt-devel
BuildRequires:  coolkey
BuildRequires:  opensc
BuildRequires:  nss-tools
BuildRequires:  nspr-devel >= 4.9.2
BuildRequires:  nss-devel >= 3.13.6
BuildRequires:  systemd

%description
This package contains the pesign utility for signing UEFI binaries as
well as other associated tools.


%prep
%setup -q -n %{name}-%{version}/upstream

# 0001-Don-t-set-SO_PASSCRED.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
make PREFIX=%{_prefix} LIBDIR=%{_libdir}
# << build pre



# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
mkdir -p %{buildroot}/%{_libdir}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} \
install
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} \
install_systemd
# << install pre

# >> install post
# there's some stuff that's not really meant to be shipped yet
rm -rf %{buildroot}/boot %{buildroot}/usr/include
rm -rf %{buildroot}%{_libdir}/libdpe*
mv rh-test-certs/etc/pki/pesign/* %{buildroot}/etc/pki/pesign/

#modutil -force -dbdir %{buildroot}/etc/pki/pesign -add coolkey \
#	-libfile %{_libdir}/pkcs11/libcoolkeypk11.so
modutil -force -dbdir %{buildroot}/etc/pki/pesign -add opensc \
-libfile %{_libdir}/pkcs11/opensc-pkcs11.so
# << install post

%pre
# >> pre
getent group pesign >/dev/null || groupadd -r pesign
getent passwd pesign >/dev/null || \
useradd -r -g pesign -d /var/run/pesign -s /sbin/nologin \
-c "Group for the pesign signing daemon" pesign
exit 0
# << pre

%files
%defattr(-,root,root,-)
%doc README TODO COPYING
%{_bindir}/pesign
%{_bindir}/pesign-client
%{_bindir}/efikeygen
%{_sysconfdir}/popt.d/pesign.popt
%{_sysconfdir}/rpm/macros.pesign
%{_mandir}/man*/*
%dir %attr(0775,pesign,pesign) /etc/pki/pesign
%attr(0664,pesign,pesign) /etc/pki/pesign/*
%dir %attr(0770, pesign, pesign) %{_localstatedir}/run/%{name}
%ghost %attr(0660, -, -) %{_localstatedir}/run/%{name}/socket
%ghost %attr(0660, -, -) %{_localstatedir}/run/%{name}/pesign.pid
%{_prefix}/lib/tmpfiles.d/pesign.conf
%{_unitdir}/pesign.service
# >> files
# << files
