# Built from the vendored Go modules, with the version stamped in as the
# release builds do.
%global debug_package %{nil}

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           lazygit
Version:        0.66.2
Release:        0.1%{?dist}
Summary:        Simple terminal UI for git commands
License:        MIT
URL:            https://github.com/jesseduffield/lazygit
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.26

Requires:       git-core

%description
A terminal UI for git that stages hunks and lines, rebases interactively,
cherry-picks and resolves conflicts from a single screen.

%prep
%autosetup

%build
go build -mod=vendor -trimpath -buildmode=pie \
    -ldflags "-X main.version=%{version} -X main.buildSource=copr" \
    -o %{name} .

%install
install -Dm0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Sun Nov 01 2026 seeweedx <git.atlas138@passmail.com> - 0.66.2-0.1
- Package upstream v0.66.2
