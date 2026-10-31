# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           fsel
Version:        4.0.0
Release:        0.1%{?dist}
Summary:        Fast TUI app launcher and fuzzy finder
License:        BSD-2-Clause
URL:            https://github.com/Mjoyufull/fsel
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  rust >= 1.94

%description
A terminal launcher for desktop applications that doubles as a dmenu-style
fuzzy picker for stdin, with a cclip clipboard history mode.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%files
%license LICENSE
%doc README.md config.toml keybinds.toml color_examples.toml
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Sun Nov 01 2026 seeweedx <git.atlas138@passmail.com> - 4.0.0-0.1
- Package upstream 4.0.0
