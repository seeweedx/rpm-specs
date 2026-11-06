# Built with Bun, which Fedora does not package, so the spec carries upstream's
# Bun release for each architecture. bun install fetches the npm dependencies
# and the build a models.dev snapshot, so the build needs network access.
#
# The result is a Bun executable, its JavaScript appended to the Bun runtime,
# which stripping would cut off, so there is no debuginfo and no strip.
%global debug_package %{nil}
%global __os_install_post %{nil}
%global _missing_build_ids_terminate_build 0

# The Bun version upstream's packageManager field names. Its build script
# refuses any older Bun, so a bump on their side fails the build here until
# this follows.
%global bun_version 1.4.4

# Release stays below 1 so a Fedora package, should one appear, replaces this.
Name:           opencode
Version:        1.19.5
Release:        0.1%{?dist}
Summary:        Open source AI coding agent for the terminal
License:        MIT
URL:            https://github.com/anomalyco/opencode
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/oven-sh/bun/releases/download/bun-v%{bun_version}/bun-linux-aarch64.zip
Source2:        https://github.com/oven-sh/bun/releases/download/bun-v%{bun_version}/bun-linux-x64.zip

ExclusiveArch:  x86_64 aarch64

# node-gyp compiles the native tree-sitter grammars bun install pulls in.
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  unzip
BuildRequires:  zsh

# opencode searches files with rg and downloads its own copy when none is on
# PATH.
Requires:       ripgrep

%description
opencode is an AI coding agent with a terminal interface. It reads and edits
files and runs commands in a project, asking before it acts, and works with
hosted providers or any OpenAI-compatible server such as llama-server.

%prep
%autosetup
%ifarch aarch64
unzip -q %{SOURCE1}
mv bun-linux-aarch64 bun
%else
unzip -q %{SOURCE2}
mv bun-linux-x64 bun
%endif

%build
export PATH=$PWD/bun:$PATH
export HUSKY=0
bun install --frozen-lockfile
cd packages/opencode
OPENCODE_VERSION=%{version} OPENCODE_CHANNEL=prod \
  bun --bun ./script/build.ts --single --skip-install

%install
install -Dm0755 packages/opencode/dist/opencode-linux-*/bin/opencode \
  %{buildroot}%{_bindir}/opencode
# yargs picks the completion script by the shell SHELL names.
SHELL=/bin/zsh HOME=$PWD %{buildroot}%{_bindir}/opencode completion \
  > _opencode
install -Dm0644 _opencode %{buildroot}%{_datadir}/zsh/site-functions/_opencode
SHELL=/bin/bash HOME=$PWD %{buildroot}%{_bindir}/opencode completion \
  > opencode.bash
install -Dm0644 opencode.bash \
  %{buildroot}%{_datadir}/bash-completion/completions/opencode

%files
%license LICENSE
%doc README.md
%{_bindir}/opencode
%{_datadir}/bash-completion/completions/opencode
%{_datadir}/zsh/site-functions/_opencode

%changelog
* Fri Nov 06 2026 seeweedx <git.atlas138@passmail.com> - 1.19.5-0.1
- Package upstream v1.19.5
