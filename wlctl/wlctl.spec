# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           wlctl
Version:        0.1.10
Release:        0.1%{?dist}
Summary:        WiFi TUI for NetworkManager
License:        GPL-3.0-only
URL:            https://github.com/aashish-thapa/wlctl
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  rust

Requires:       NetworkManager

%description
A terminal interface for WiFi, Ethernet and WireGuard connections that talks
to NetworkManager over D-Bus, in the style of impala.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc Readme.md CHANGELOG.md
%{_bindir}/%{name}

%changelog
* Sun Nov 01 2026 seeweedx <git.atlas138@passmail.com> - 0.1.10-0.1
- Package upstream v0.1.10
