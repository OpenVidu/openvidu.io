#!/bin/bash
set -e

# This script completely overwrites the latest version of the
# documentation, also updating the non-versioned pages located at root

# Check if mike is installed
command -v mike >/dev/null 2>&1 || {
    echo >&2 "mike not found. Install it with \"pip install mike\""
    exit 1
}

# If there is no version passed to the script as an argument, exit
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 X.Y.Z"
    exit 1
else
    VERSION=$1
fi

# Navigate to the root of the repository based on the script location
cd "$(dirname "$0")" || exit
cd ..

# Delete the version in gh-pages branch
mike delete --push "${VERSION}" || {
    echo 'Failure deleting version with mike'
    exit 1
}
# Publish again
echo "Overwriting latest version ${VERSION}"
cd ./custom-versioning
source ./push-new-version.sh "${VERSION}"

# Merge latest commits of main into VERSION branch. This keeps the latest VERSION branch up to date with main
git switch "${VERSION}"
git rebase main
git push --force
git switch main