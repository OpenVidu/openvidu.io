#!/usr/bin/env bash
#
# Run ONLY the post-processing half of the shell implementation against a directory.
#
# push-new-version.sh calls `main "$@"` on its last line, so it cannot simply be sourced.
# This strips that line, sources the rest to get the functions and the page arrays, then
# replays the body of `updateWebsite` — minus every git operation, so the comparison is
# about the tree and nothing else.
#
# Usage:
#   run_old_postprocess.sh VERSION {true|false} TREE LEGACY_DIR
#
# LEGACY_DIR holds a checkout of the pre-migration custom-versioning/ folder, extracted from
# git by run_parity.sh. Keeping the shell implementation in git history rather than vendoring
# a copy here means the oracle is the real thing, not a snapshot someone has to remember to
# update.

set -e

VERSION="$1"
UPDATE_LATEST="$2"
TREE="$(cd "$3" && pwd)"
LEGACY_DIR="$(cd "$4" && pwd)"

REDIRECT_HTML="$LEGACY_DIR/redirect-from-version-to-getting-started.html"
LEGACY_SCRIPT="$LEGACY_DIR/push-new-version.sh"

for required in "$LEGACY_SCRIPT" "$REDIRECT_HTML" "$LEGACY_DIR/copy-releases-content.py"; do
    [ -f "$required" ] || {
        echo "run_old_postprocess.sh: missing $required" >&2
        exit 1
    }
done

# The helper the shell invoked through a mktemp copy, for the same reason it did: the path
# must survive independently of the tree being rewritten.
RELEASES_CONTENT_HELPER="$(mktemp)"
trap 'rm -f "$RELEASES_CONTENT_HELPER" "$SOURCEABLE"' EXIT
cp "$LEGACY_DIR/copy-releases-content.py" "$RELEASES_CONTENT_HELPER"

SOURCEABLE="$(mktemp)"
grep -v '^main \$@$' "$LEGACY_SCRIPT" >"$SOURCEABLE"
# shellcheck disable=SC1090
. "$SOURCEABLE"

cd "$TREE"

# --- the body of updateWebsite, with the git calls removed ---------------------------------

rm -rf site
rm -rf "$VERSION/overrides"

# The shell restored this from a branch with `git restore`; here it is handed in directly. The
# folder name is the historical one, not a stale rename: it is where the shell put the file, and
# the point of this script is to reproduce the shell exactly.
mkdir -p custom-versioning
cp "$REDIRECT_HTML" custom-versioning/redirect-from-version-to-getting-started.html

changeVersionedPagesLinks
changeSearchIndexLinks

if [ "$UPDATE_LATEST" = false ]; then
    rm -rf "${NON_VERSIONED_PAGES[@]/#/$VERSION/}"
    rm "$VERSION/404.html" || true
    rm "$VERSION/index.md" || true
    rm "$VERSION/robots.txt" || true
    rm "$VERSION/llms.txt" || true
    rm "$VERSION/llms-full.txt" || true
    rm "$VERSION/feed_rss_created.xml" || true
    rm "$VERSION/feed_rss_updated.xml" || true
    rm "$VERSION/feed_json_created.json" || true
    rm "$VERSION/feed_json_updated.json" || true
    rm "$VERSION/rss.xsl" || true

    mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"
    updateVersionSitemap

    LATEST_VERSION=$(readlink latest 2>/dev/null || true)
    if [ -n "$LATEST_VERSION" ]; then
        copyReleasesFromTo "$LATEST_VERSION" "$VERSION"
    else
        echo "run_old_postprocess.sh: could not resolve the 'latest' symlink" >&2
    fi
else
    changeNonVersionedPagesLinks
    copyFilesFromVersionToRoot
    mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"
    updateSitemap
    updateVersionSitemap
    copyReleasesToAllOtherVersions
fi

# The shell left this folder behind for `git add .` to ignore; remove it so it does not show
# up as a difference against a run that never created it.
rmdir custom-versioning 2>/dev/null || true

echo "run_old_postprocess.sh: done ($VERSION, update_latest=$UPDATE_LATEST)"
