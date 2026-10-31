# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           otter-launcher
Version:        0.8.2
Release:        0.1%{?dist}
Summary:        Terminal launcher that runs commands through shell modules
License:        GPL-3.0-only
URL:            https://github.com/kuokuo123/otter-launcher
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust

%description
A terminal launcher in the spirit of dmenu, whose modules run shell commands
with the typed prompt, and which can show images and ANSI art beside it.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}
cp -a contrib %{buildroot}%{_datadir}/%{name}/

%files
%license LICENSE
%doc README.md config_example
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Sat Oct 31 2026 seeweedx <git.atlas138@passmail.com> - 0.8.2-0.1
- Package upstream v0.8.2
