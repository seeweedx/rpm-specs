# rpm-specs

Spec files for the [seaweed COPRs](https://copr.fedorainfracloud.org/coprs/seaweed/),
one project per package, built from source for Fedora on aarch64 and x86_64.

| Package | Install |
| --- | --- |
| bluetui | `dnf copr enable seaweed/bluetui` |
| cclip | `dnf copr enable seaweed/cclip` |
| fsel | `dnf copr enable seaweed/fsel` |
| keepassxc | `dnf copr enable seaweed/keepassxc` |
| lazygit | `dnf copr enable seaweed/lazygit` |
| llama-cpp | `dnf copr enable seaweed/llama-cpp` |
| opencode | `dnf copr enable seaweed/opencode` |
| otter-launcher | `dnf copr enable seaweed/otter-launcher` |
| starship | `dnf copr enable seaweed/starship` |
| wlctl | `dnf copr enable seaweed/wlctl` |
| xdg-desktop-portal-termfilechooser | `dnf copr enable seaweed/xdg-desktop-portal-termfilechooser` |
| yazi | `dnf copr enable seaweed/yazi` |

Releases start at `0.1`, so a package Fedora ships itself replaces these.

## Updates

`.github/workflows/update.yml` runs `update.sh` daily. For every package in
`upstream.tsv` whose upstream has a newer GitHub release, it sets `Version`,
resets `Release` to `0.1`, adds a changelog entry and commits. After pushing,
it calls each bumped package's COPR custom webhook, listed one per line as
`<package> <url>` in the `COPR_WEBHOOKS` secret. Running the workflow by hand
with `rebuild` set to package names rebuilds those without a bump.

COPR builds each package from this repository with the `make_srpm` method:
`.copr/Makefile` downloads the spec's sources and packs the SRPM.
