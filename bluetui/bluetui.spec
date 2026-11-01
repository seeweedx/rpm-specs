# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access. It
# builds libdbus from the copy libdbus-sys vendors, so dbus-devel is not needed.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           bluetui
Version:        0.8.2
Release:        0.1%{?dist}
Summary:        Bluetooth TUI for BlueZ
License:        GPL-3.0-only
URL:            https://github.com/pythops/bluetui
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  rust

Requires:       bluez

%description
A terminal interface for pairing, connecting and trusting Bluetooth devices
that talks to BlueZ over D-Bus.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc Readme.md
%{_bindir}/%{name}

%changelog
* Mon Nov 02 2026 seeweedx <git.atlas138@passmail.com> - 0.8.2-0.1
- Package upstream v0.8.2
