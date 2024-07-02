#!/bin/bash

# This script completely overwrites the latest version of the documentation
# It updates the non-versioned pages of the documentation located at root

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

mike delete --push "${VERSION}"
source ./custom-versioning/push-new-version.sh "${VERSION}"