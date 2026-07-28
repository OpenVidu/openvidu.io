#!/usr/bin/env bash
#
# The parity gate: prove that `ovweb postprocess` turns a built tree into the same published
# tree the shell implementation did.
#
# The two runs share ONE `mike` build, so nothing that varies between builds — timestamps,
# privacy-plugin downloads, image optimisation — can enter the comparison. What is left is
# purely the post-processing, which is the thing being replaced.
#
# Usage:
#   run_parity.sh [VERSION] [latest|past]
#
# Environment:
#   LEGACY_REF   git ref holding the shell implementation. Defaults to the pinned commit below,
#                which stays reachable forever, so this normally needs no setting.
#   WORK         working directory (default: a fresh mktemp -d).
#   OVWEB        the ovweb entry point (default: `ovweb` on PATH).
#
# Requirements: mike and the publishing dependencies, i.e.
#   pip install "./publish-tool[build]"
#
# Each run keeps a clone plus three copies of the built tree — a few GB. WORK is reused between
# runs of the same version, but remove it when you are done.
#
# Run the whole matrix before merging:
#   run_parity.sh 3.99 latest     # a new minor, root pages refreshed
#   run_parity.sh 3.8  latest     # the current newest, rebuilt in place
#   run_parity.sh 3.2  past       # an old minor built by an older configuration

set -euo pipefail

VERSION="${1:-3.99}"
MODE="${2:-latest}"

# The last commit that still contains custom-versioning/push-new-version.sh — the shell
# implementation this tool replaced, and the oracle this gate compares against. Pinned to a
# SHA rather than a branch on purpose: a branch name would stop resolving the moment the
# migration merged, and nobody would remember which commit to use instead. The commit stays
# reachable in history, so this keeps working indefinitely.
LEGACY_REF="${LEGACY_REF:-588216ecb}"
OVWEB="${OVWEB:-ovweb}"

case "$MODE" in
latest) UPDATE_LATEST=true ;;
past) UPDATE_LATEST=false ;;
*)
    echo "run_parity.sh: mode must be 'latest' or 'past', got '$MODE'" >&2
    exit 2
    ;;
esac

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
WORK="${WORK:-$(mktemp -d -t ovweb-parity-XXXXXX)}"
mkdir -p "$WORK"

echo "==> version=$VERSION mode=$MODE legacy=$LEGACY_REF"
echo "==> work=$WORK"

# 1. A throwaway clone, so nothing here can touch the real repository or its remote.
if [ ! -d "$WORK/repo" ]; then
    git clone --no-local --quiet "$REPO" "$WORK/repo"
    git -C "$WORK/repo" fetch --quiet origin 'refs/heads/*:refs/heads/*' 2>/dev/null || true
fi
CLONE="$WORK/repo"

# 2. The shell implementation, taken from git rather than vendored.
LEGACY_DIR="$WORK/legacy"
if [ ! -d "$LEGACY_DIR" ]; then
    mkdir -p "$LEGACY_DIR"
    for file in push-new-version.sh copy-releases-content.py \
        redirect-from-version-to-getting-started.html; do
        git -C "$CLONE" show "$LEGACY_REF:custom-versioning/$file" >"$LEGACY_DIR/$file" || {
            echo "run_parity.sh: $file is not in $LEGACY_REF." >&2
            echo "Set LEGACY_REF to a commit from before the migration." >&2
            exit 1
        }
    done
    chmod +x "$LEGACY_DIR/push-new-version.sh"
fi

# For a past version the content comes from that version's own branch, which is also what
# mike must build from.
if [ "$UPDATE_LATEST" = false ]; then
    git -C "$CLONE" switch --quiet "$VERSION"
fi

# 3. ONE build. `mike deploy` without --push commits to the local gh-pages only.
echo "==> building $VERSION with mike (this is the only build; both runs share it)"
# CI=false keeps the privacy and optimize plugins off, matching validate-web.yaml: they fetch
# external assets and re-encode images, neither of which the post-processing looks at.
if ! (cd "$CLONE" && CI=false mike deploy "$VERSION" >"$WORK/build.log" 2>&1); then
    echo "run_parity.sh: the build failed. Last lines of $WORK/build.log:" >&2
    tail -30 "$WORK/build.log" >&2
    exit 1
fi

# 4. The raw output, before any post-processing.
rm -rf "$WORK/raw" "$WORK/old" "$WORK/new"
git -C "$CLONE" worktree add --quiet "$WORK/raw" gh-pages
cp -a "$WORK/raw" "$WORK/old"
cp -a "$WORK/raw" "$WORK/new"
rm -rf "$WORK/old/.git" "$WORK/new/.git"

# 5. The shell implementation.
echo "==> running the shell post-processing on $WORK/old"
"$HERE/run_old_postprocess.sh" "$VERSION" "$UPDATE_LATEST" "$WORK/old" "$LEGACY_DIR"

# 6. ovweb.
echo "==> running ovweb postprocess on $WORK/new"
LATEST_FLAG=$([ "$UPDATE_LATEST" = true ] && echo --update-latest || echo --no-update-latest)
"$OVWEB" --layout "$REPO/publish-tool/ovweb.yaml" postprocess \
    "$VERSION" --tree "$WORK/new" "$LATEST_FLAG"

# 7. Compare.
echo "==> comparing"
set +e
python3 "$HERE/compare.py" "$WORK/old" "$WORK/new" "$VERSION"
STATUS=$?
set -e

git -C "$CLONE" worktree remove --force "$WORK/raw" 2>/dev/null || true

if [ "$STATUS" -ne 0 ]; then
    echo
    echo "Parity FAILED. Inspect the two trees:"
    echo "  diff -r --no-dereference $WORK/old $WORK/new"
    exit "$STATUS"
fi
echo "Parity OK for $VERSION ($MODE)."
