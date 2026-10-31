# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           xdg-desktop-portal-termfilechooser
Version:        1.5.0
Release:        0.1%{?dist}
Summary:        xdg-desktop-portal backend for choosing files with a terminal file manager
License:        MIT
URL:            https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.60.0
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  scdoc >= 1.9.7
BuildRequires:  systemd-rpm-macros

Requires:       dbus-common
Requires:       xdg-desktop-portal
Enhances:       xdg-desktop-portal

%description
A backend for xdg-desktop-portal that hands the FileChooser interface to a
terminal file manager such as yazi, ranger, lf, nnn or vifm, through the
wrapper scripts it ships.

%prep
%autosetup

%build
%meson -Dsd-bus-provider=libsystemd -Dsystemd=enabled -Dman-pages=enabled
%meson_build

%install
%meson_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md Compatibility.md
%{_libexecdir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.termfilechooser.service
%{_datadir}/xdg-desktop-portal/portals/termfilechooser.portal
%{_userunitdir}/%{name}.service
%{_mandir}/man5/%{name}.5*

%changelog
* Sat Oct 31 2026 seeweedx <git.atlas138@passmail.com> - 1.5.0-0.1
- Package upstream v1.5.0
