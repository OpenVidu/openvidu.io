#!/bin/bash
set -e

# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "conditions" "blog") # And root index.html and 404.html
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

ALL_PREFIXED_NVP="${NON_VERSIONED_PAGES[@]/#/$VERSION/}"
ALL_PREFIXED_VP="${VERSIONED_PAGES[@]/#/$VERSION/}"

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
        echo "The branch '$VERSION_BRANCH' does not exist. To update a past version, the branch must exist"
        exit 1
    else
        echo "Git branch '$VERSION_BRANCH' does not exist in the remote repository. Creating it"
        git checkout -b "$VERSION_BRANCH"
        git push -u origin "$VERSION_BRANCH"
    fi
fi

if [ "$UPDATE_LATEST" = true ]; then
    # Build and deploy the new version with mike, updating latest alias
    mike deploy --push --update-aliases "$VERSION" latest
    echo "New version $VERSION published with mike (latest alias updated to this new version)"
else
    # Build and deploy the new version with mike
    mike deploy --push "$VERSION"
    echo "New version $VERSION published with mike (latest alias not updated)"
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

# Delete overrides folder in the new version
rm -rf "$VERSION/overrides"

# Modify all links in VP that point to NVP to use absolute links ("/NVP/")
for NVP in "${NON_VERSIONED_PAGES[@]}"; do
    grep -Erl "href=\"(\.\./)*$NVP/" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*$NVP/|href=\"/$NVP/|g"
done

# Links to index.html
grep -Erl "\"(\.\./)*\.\.\"" $ALL_PREFIXED_VP | xargs sed -i "s|\"\(\.\./\)*\.\.\"|\"/\"|g"

# Remove version from NVP in sitemap.xml
for NVP in "${NON_VERSIONED_PAGES[@]}"; do
    sed -i "s|$VERSION/$NVP|$NVP|g" "$VERSION/sitemap.xml"
done

# Remove version from root in sitemap.xml
sed -i "s|$VERSION/</loc>|</loc>|g" "$VERSION/sitemap.xml"

# Regenerate sitemap.xml.gz
gzip -k -f "$VERSION/sitemap.xml"

# Modify links in search_index.json to use absolute links
# Modify all links to VP to use absolute links including the version ("/X.Y.Z/VP/")
for VP in "${VERSIONED_PAGES[@]}"; do
    sed -i "s|\"location\":\"$VP/|\"location\":\"/$VERSION/$VP/|g" "$VERSION/search/search_index.json"
done

# Modify all links to NVP to use absolute links ("/NVP/")
for NVP in "${NON_VERSIONED_PAGES[@]}"; do
    sed -i "s|\"location\":\"$NVP/|\"location\":\"/$NVP/|g" "$VERSION/search/search_index.json"
done

# Modify all links to root to use absolute links ("/")
sed -i "s|\"location\":\"\"|\"location\":\"/\"|g" "$VERSION/search/search_index.json"

if [ "$UPDATE_LATEST" = false ]; then
    echo "The latest version will not be updated"

    # Remove NVP from new version
    rm -rf $ALL_PREFIXED_NVP
    rm "$VERSION/index.html"
    rm "$VERSION/404.html"

    # Commit the updated version folder
    git add .
    git commit -am "Version $VERSION updated. Non-versioned pages untouched"
else
    echo "The latest version will be updated"

    # Remove version in all links of 404.html
    sed -i "s|/$VERSION/|/|g" "$VERSION/404.html"
    sed -i "s|\"/$VERSION\"|\"/\"|g" "$VERSION/404.html"

    for VP in "${VERSIONED_PAGES[@]}"; do
        sed -i "s|href=\"/$VP/|href=\"/latest/$VP/|g" "$VERSION/404.html"
    done

    # Modify all links in NVP that point to VP to use absolute links to the latest version ("/latest/VP/")
    for VP in "${VERSIONED_PAGES[@]}"; do
        grep -Erl "href=\"(\.\./)*$VP/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|href=\"\(\.\./\)*$VP/|href=\"/latest/$VP/|g"
    done

    # Remove version in the canonical tag of NVP
    grep -Erl "$VERSION/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|$VERSION/||g"

    # Copy asset folders to root
    for asset in "${ASSETS[@]}"; do
        # Delete previous root version of the asset folder
        rm -rf "$asset"
        # Copy the new version of the asset folder to root
        cp -r "$VERSION/$asset" .
    done

    # Move NVP to root
    mv "$VERSION/index.html" . # Home page
    mv "$VERSION/404.html" . # 404 page

    for NVP in "${NON_VERSIONED_PAGES[@]}"; do # Other NVP
        # Delete previous root version of the page
        rm -rf "$NVP"
        # Move new page as their root version
        mv "$VERSION/$NVP" .
    done

    git add .
    git commit -am "Version $VERSION updated. Non-versioned pages updated"
fi

git push --set-upstream origin "$GH_BRANCH"

git checkout main

echo "Success publishing documentation for version $VERSION!"
