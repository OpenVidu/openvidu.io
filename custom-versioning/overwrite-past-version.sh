#!/bin/bash
set -e

# This script overwrites a specific past version of the documentation
# without updating the non-versioned pages located at root

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

# Check if the current git tag exactly matches the version
# CURRENT_GIT_TAG=$(git describe --tags --abbrev=0)
# if [ "$CURRENT_GIT_TAG" != "$VERSION" ]; then
#     echo "The current git tag does not match version $VERSION (current tag is $CURRENT_GIT_TAG)"
#     echo "To overwrite a past version the local repository must be checked out at this specific tag"
#     exit 1
# fi

# Delete the version in gh-pages branch
mike delete --push "${VERSION}" || {
    echo 'Failure deleting version with mike'
    exit 1
}
# Publish again
echo "Overwriting past version ${VERSION}"
cd ./custom-versioning
source ./push-new-version.sh "${VERSION}" false
