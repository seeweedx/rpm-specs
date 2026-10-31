# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           yazi
Version:        26.9.1
Release:        0.1%{?dist}
Summary:        Blazing fast terminal file manager
License:        MIT
URL:            https://github.com/sxyazi/yazi
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  rust >= 1.95

# yazi asks file(1) for MIME types.
Requires:       file

%description
A terminal file manager written in Rust on non-blocking async I/O, with image
previews, a Lua plugin system and a package manager for plugins and flavors.
Includes ya, its command-line companion.

%prep
%autosetup

%build
cargo build --release --locked -p yazi-fm -p yazi-cli

%install
install -Dm0755 target/release/yazi %{buildroot}%{_bindir}/yazi
install -Dm0755 target/release/ya %{buildroot}%{_bindir}/ya
desktop-file-install --dir=%{buildroot}%{_datadir}/applications assets/yazi.desktop
install -Dm0644 assets/logo.png %{buildroot}%{_datadir}/pixmaps/yazi.png

%files
%license LICENSE LICENSE-ICONS
%doc README.md
%{_bindir}/yazi
%{_bindir}/ya
%{_datadir}/applications/yazi.desktop
%{_datadir}/pixmaps/yazi.png

%changelog
* Sun Nov 01 2026 seeweedx <git.atlas138@passmail.com> - 26.9.1-0.1
- Package upstream v26.9.1
