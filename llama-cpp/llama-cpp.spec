# Fedora's llama-cpp builds only the CPU backend on aarch64, as its Vulkan
# backend is switched off for every architecture. This one adds Vulkan, which
# runs on Asahi's Honeykrisp driver, and loads backends as plugins from
# %%{_libdir}/ggml, where every CPU variant waits for the one the machine can run.
#
# Upstream's semantic versions sort above Fedora's b-prefixed build numbers,
# so this replaces Fedora's package, sonames included, until Fedora adopts them.
# Release stays below 1 so a Fedora build of the same version would win.
Name:           llama-cpp
Version:        1.0.0
Release:        0.1%{?dist}
Summary:        LLM inference in C/C++ with the Vulkan backend
License:        MIT
URL:            https://github.com/ggml-org/llama.cpp
Source0:        %{url}/archive/v%{version}/llama.cpp-%{version}.tar.gz
# The server embeds a web UI that the build otherwise fetches from Hugging Face,
# which COPR's offline builders cannot reach. Upstream publishes it only with
# the nightly build a release was cut from; update.sh keeps nightly in step.
%global nightly b12359
Source1:        %{url}/releases/download/%{nightly}/llama-%{nightly}-ui.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  glslc
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  spirv-headers-devel

Provides:       bundled(cpp-httplib)
Provides:       bundled(miniaudio)
Provides:       bundled(nlohmann-json)
Provides:       bundled(stb)

%description
Inference of large language models in plain C/C++ through ggml, with the
llama-server OpenAI-compatible server and its web UI, llama-cli, and tools to
benchmark, quantize and convert models. Built with the Vulkan backend and
every CPU variant, loaded at runtime.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake and pkg-config files for linking against libllama, libmtmd and
libggml.

%prep
%autosetup -n llama.cpp-%{version}
mkdir tools/ui/dist
tar -xzf %{SOURCE1} -C tools/ui/dist --strip-components=1

%build
%cmake \
    -DGGML_NATIVE=OFF \
    -DGGML_BACKEND_DL=ON \
    -DGGML_BACKEND_DIR=%{_libdir}/ggml \
    -DGGML_CPU_ALL_VARIANTS=ON \
    -DGGML_VULKAN=ON \
    -DGGML_CCACHE=OFF \
    -DLLAMA_BUILD_IS_DEV=OFF \
    -DLLAMA_BUILD_NUMBER=%{sub %{nightly} 2 -1} \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_USE_PREBUILT_UI=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE licenses/LICENSE-jsonhpp
%doc README.md
%{_bindir}/llama
%{_bindir}/llama-*
%{_libdir}/libggml-base.so.*
%{_libdir}/libggml.so.*
%{_libdir}/libllama.so.*
%{_libdir}/libllama-common.so.*
%{_libdir}/libmtmd.so.*
# Private libraries behind the unified llama binary, without a soname version.
%{_libdir}/libllama-*-impl.so
%{_libdir}/ggml/

%files devel
%{_includedir}/ggml*.h
%{_includedir}/gguf.h
%{_includedir}/llama*.h
%{_includedir}/mtmd*.h
%{_libdir}/libggml-base.so
%{_libdir}/libggml.so
%{_libdir}/libllama.so
%{_libdir}/libllama-common.so
%{_libdir}/libmtmd.so
%{_libdir}/cmake/ggml/
%{_libdir}/cmake/llama/
%{_libdir}/pkgconfig/llama.pc

%changelog
* Fri Nov 13 2026 seeweedx <git.atlas138@passmail.com> - 1.0.0-0.1
- Update to upstream v1.0.0

* Fri Nov 06 2026 seeweedx <git.atlas138@passmail.com> - 0.9.0-0.1
- Package upstream v0.9.0 with the Vulkan backend
