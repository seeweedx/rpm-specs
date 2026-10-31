# Built with cargo against crates.io rather than Fedora's rust-* packages, which
# do not carry all of its dependencies, so the build needs network access.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           starship
Version:        1.27.0
Release:        0.1%{?dist}
Summary:        Minimal, fast and customizable prompt for any shell
License:        ISC
URL:            https://github.com/starship/starship
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  rust >= 1.95

%description
A cross-shell prompt that shows the state of the directory it is in, such as
the git branch and the language versions in use, configured in TOML.

%prep
%autosetup

%build
cargo build --release --locked

%install
install -Dm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -d %{buildroot}%{bash_completions_dir} %{buildroot}%{zsh_completions_dir} %{buildroot}%{fish_completions_dir}
target/release/%{name} completions bash > %{buildroot}%{bash_completions_dir}/%{name}
target/release/%{name} completions zsh > %{buildroot}%{zsh_completions_dir}/_%{name}
target/release/%{name} completions fish > %{buildroot}%{fish_completions_dir}/%{name}.fish

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
* Sun Nov 01 2026 seeweedx <git.atlas138@passmail.com> - 1.27.0-0.1
- Package upstream v1.27.0
