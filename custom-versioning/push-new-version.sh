#!/bin/bash
set -e

# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "conditions" "blog")
VERSIONED_PAGES=("docs")

# Check if mike is installed
command -v mike >/dev/null 2>&1 || {
    echo >&2 "mike not found. Install it with \"pip install mike\""
    exit 1
}

# If there is no version passed to the script as an argument, exit
if [ $# -lt 1 ]; then
    echo "Usage: $0 X.Y.Z"
    exit 1
else
    VERSION=$1
    echo "Publishing new version $VERSION"
    UPDATE_LATEST=${2:-true}
    if [ "$UPDATE_LATEST" = true ]; then
        echo "The latest version will be updated"
    elif [ "$UPDATE_LATEST" = false ]; then
        echo "The latest version will not be updated"
    else
        echo "Second argument must be a boolean if provided: $0 X.Y.Z false"
        exit 1
    fi
fi

# Navigate to the root of the repository based on the script location
cd "$(dirname "$0")" || exit
cd ..

if [[ $(git status --porcelain) ]]; then
    echo "There are uncommitted changes in the repository. Please commit or stash them before running this script"
    exit 1
fi

# If branch gh-pages exists in the remote repository, pull changes
GH_BRANCH="gh-pages"
# Check if the branch exists in the remote repository with git ls-remote
if git ls-remote --heads origin "$GH_BRANCH" | grep -q "$GH_BRANCH"; then
    echo "Git branch '$GH_BRANCH' exists in the remote repository"
    git checkout "$GH_BRANCH"
    git pull origin "$GH_BRANCH"
    git checkout main
else
    echo "Git branch '$GH_BRANCH' does not exist in the remote repository. This is the first version deployment"
fi

# If the version branch exists in the remote repository, pull changes. If not, create it
VERSION_BRANCH="${VERSION}"
# Check if the branch exists in the remote repository with git ls-remote
if git ls-remote --heads origin "$VERSION_BRANCH" | grep -q "$VERSION_BRANCH"; then
    echo "Git branch '$VERSION_BRANCH' exists in the remote repository"
    git checkout "$VERSION_BRANCH"
    git pull origin "$VERSION_BRANCH"
    if [ "$UPDATE_LATEST" = true ]; then
        git checkout main
    fi
else
    if [ "$UPDATE_LATEST" = false ]; then
        echo "The branch ${VERSION_BRANCH} does not exist. To update a past version, the branch must exist"
        exit 1
    else
        echo "Git branch '$VERSION_BRANCH' does not exist in the remote repository. Creating it"
        git checkout -b "$VERSION_BRANCH"
        git push -u origin "$VERSION_BRANCH"
    fi
fi

if [ "$UPDATE_LATEST" = true ]; then
    # Build and deploy the new version with mike, updating latest alias
    mike deploy --push --update-aliases "${VERSION}" latest
    # Set the default version to latest
    mike set-default --push latest
    echo "New version ${VERSION} published with mike (latest alias updated to this new version)"
else
    # Build and deploy the new version with mike
    mike deploy --push "${VERSION}"
    echo "New version ${VERSION} published with mike (latest alias not updated)"
fi

# Checkout to gh-pages branch
git checkout "$GH_BRANCH" || {
    echo "Failure checking out to $GH_BRANCH"
    exit 1
}

# Pull again for remote changes
git pull origin "$GH_BRANCH" || {
    echo "Failure pulling from remote $GH_BRANCH"
    exit 1
}

# Delete site folder
rm -rf site

# Copy necessary files from main branch
git restore --source main custom-versioning/. || {
    echo 'Failure copying files from main branch'
    exit 1
}

# Wait until this file exists in branch gh-pages
until [ -f ./custom-versioning/redirect-from-version-to-root.html ]; do
    sleep 1
done

if [ "$UPDATE_LATEST" = false ]; then

    echo "The latest version will not be updated"

    # Overwrite the non-versioned pages inside /X.Y.Z/ with redirections to root
    # E.g. allows redirecting from https://openvidu.io/3.0.0/pricing to https://openvidu.io/pricing
    for page in "${NON_VERSIONED_PAGES[@]}"; do
        NON_VERSIONED_HTMLS=$(find "./${VERSION}"/"${page}" -iname 'index.html')
        for html in $NON_VERSIONED_HTMLS; do
            cp ./custom-versioning/redirect-from-version-to-root.html "${html}"
        done
    done

    # Commit the updated version folder
    git add "${VERSION}"
    git commit -am "Version ${VERSION} updated. Non-versioned pages untouched"

else

    echo "The latest version will be updated"

    # Copy asset folders to root
    for asset in "${ASSETS[@]}"; do
        # Delete previous root version of the asset folder
        rm -rf "${asset}"
        # Copy the new version of the asset folder to root
        cp -r "${VERSION}"/"${asset}" .
    done

    # Copy non-versioned pages to root
    cp "${VERSION}"/index.html . # Home page
    cp ./custom-versioning/redirect-from-version-to-root.html "${VERSION}"/index.html
    for page in "${NON_VERSIONED_PAGES[@]}"; do # Other non-versioned pages
        # Delete previous root version of the page
        rm -rf "${page}"
        # Copy new page as their root version
        cp -r "${VERSION}"/"${page}" .
        # Overwrite the non-versioned pages inside /X.Y.Z/ with redirections to root
        # E.g. allows redirecting from https://openvidu.io/3.0.0/pricing to https://openvidu.io/pricing
        NON_VERSIONED_HTMLS=$(find "./${VERSION}"/"${page}" -iname 'index.html')
        for html in $NON_VERSIONED_HTMLS; do
            cp ./custom-versioning/redirect-from-version-to-root.html "${html}"
        done
    done

    # Create redirections to latest for versioned pages in root
    for page in "${VERSIONED_PAGES[@]}"; do
        # Delete previous root version of the page
        rm -rf "${page}"
        # Copy the new version of the page to root
        cp -r "${VERSION}"/"${page}" .
        # Overwrite the root pages with redirections to latest
        # E.g. allows redirecting from https://openvidu.io/docs/getting-started to https://openvidu.io/latest/docs/getting-started
        REDIRECTION_FOR_DOCS=$(find "./${page}" -iname 'index.html')
        for html in $REDIRECTION_FOR_DOCS; do
            cp ./custom-versioning/redirect-from-root-to-latest.html "${html}"
        done
    done

    # Commit asset folders
    for asset in "${ASSETS[@]}"; do
        git add "${asset}"
    done
    # Commit the new version folder
    git add "${VERSION}"
    # Commit home page
    git add index.html
    # Commit other non-versioned pages
    for page in "${NON_VERSIONED_PAGES[@]}"; do
        git add "${page}"
    done
    # Commit versioned pages
    for page in "${VERSIONED_PAGES[@]}"; do
        git add "${page}"
    done

    git commit -am "Version ${VERSION} updated. Non-versioned pages updated"

fi

# Remove unnecessary files from gh-pages branch
rm -rf custom-versioning

git push --set-upstream origin "$GH_BRANCH"

git checkout main

echo "Success publishing documentation for version ${VERSION}!"
