#!/usr/bin/env bash
# Bump each spec in upstream.tsv to its upstream's latest GitHub release, one
# commit per package, and print the name of every package it bumped. Release
# goes back to 0.1, which keeps it below a Fedora package should one appear.
set -euo pipefail
cd "$(dirname "$0")"

author='seeweedx <git.atlas138@passmail.com>'
date=$(LC_ALL=C date -u '+%a %b %d %Y')

while IFS=$'\t' read -r name repo prefix; do
	[[ -z $name || $name == '#'* ]] && continue
	spec=$name/$name.spec
	if ! tag=$(curl -fsSL -H "Authorization: Bearer $GITHUB_TOKEN" \
		"https://api.github.com/repos/$repo/releases/latest" | jq -er .tag_name); then
		echo "::warning::$name: no latest release from $repo" >&2
		continue
	fi
	latest=${tag#"$prefix"}
	current=$(rpmspec -q --srpm --qf '%{version}' "$spec")
	newer=$(rpm --eval "%{lua:print(rpm.vercmp('$latest', '$current'))}")
	[[ $newer == 1 ]] || continue

	# llama.cpp ships its prebuilt web UI only with the nightly build a release
	# was cut from, which the release names in nightly-tag.txt.
	if grep -q '^%global nightly ' "$spec"; then
		if ! nightly=$(curl -fsSL "https://github.com/$repo/releases/download/$tag/nightly-tag.txt"); then
			echo "::warning::$name: no nightly-tag.txt in $tag" >&2
			continue
		fi
		sed -i -E "s/^(%global nightly ).*/\1$nightly/" "$spec"
	fi

	sed -i -E "s/^(Version:[[:space:]]+).*/\1$latest/; s/^(Release:[[:space:]]+)[^%]*/\10.1/" "$spec"
	sed -i "/^%changelog$/a * $date $author - $latest-0.1\n- Update to upstream $tag\n" "$spec"
	git add "$spec"
	git commit -q -m "$name: update to $latest"
	echo "$name"
done < upstream.tsv
