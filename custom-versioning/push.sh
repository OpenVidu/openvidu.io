#!/bin/bash
#
# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

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

# If branch gh-pages exists in the remote repository, pull changes
BRANCH="gh-pages"
git ls-remote --exit-code --heads origin $BRANCH >/dev/null 2>&1
if [[ $? == '0' ]]; then
    echo "Git branch '$BRANCH' exists in the remote repository"
    git checkout gh-pages
    git pull origin gh-pages
    git checkout main
else
    echo "Git branch '$BRANCH' does not exist in the remote repository"
fi

# Build the new version with mike
mike deploy --push --update-aliases "${VERSION}" latest
# Set the default version to latest
mike set-default --push latest

# Checkout to gh-pages branch
git checkout gh-pages
# Pull again for remote changes
git pull origin gh-pages

# Copy necessary files from main branch
git checkout main -- custom-versioning/.

# Delete site folder
rm -rf site

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "conditions" "blog")
VERSIONED_PAGES=("docs")

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
    NON_VERSIONED_HTMLS=$(find "./${VERSION}"/"${page}" -iname 'index.html')
    for html in $NON_VERSIONED_HTMLS; do
        # Overwrite the versioned pages with redirections to root
        cp ./custom-versioning/redirect-from-version-to-root.html "${html}"
    done
done

# Create redirections for docs
for page in "${VERSIONED_PAGES[@]}"; do
    # Delete previous root version of the page
    rm -rf "${page}"
    # Copy the new version of the asset folder to root
    cp -r "${VERSION}"/"${page}" .
    REDIRECTION_FOR_DOCS=$(find "./docs" -iname 'index.html')
    for html in $REDIRECTION_FOR_DOCS; do
        # Overwrite the root pages with redirections to latest
        cp ./custom-versioning/redirect-from-root-to-latest.html "${html}"
    done
done

for asset in "${ASSETS[@]}"; do # Commit asset folders
    git add "${asset}"
done

# Remove unnecessary files from main branch
git reset custom-versioning/.
rm -rf custom-versioning

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

git commit -am "Overwrite non-versioned pages for ${VERSION}"
git push --set-upstream origin gh-pages

git checkout main
