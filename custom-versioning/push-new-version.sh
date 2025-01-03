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

# Copy necessary file from main branch to gh-pages branch in root
git restore --source main custom-versioning/redirect-from-version-to-getting-started.html || {
    echo 'Failure copying file from main branch'
    exit 1
}

# Wait until this file exists in branch gh-pages
until [ -f ./custom-versioning/redirect-from-version-to-getting-started.html ]; do
    sleep 1
done

# Modify all links in VP that point to NVP to use absolute links ("/NVP/")
for NVP in "${NON_VERSIONED_PAGES[@]}"; do
    grep -Erl "href=\"(\.\./)*$NVP/" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*$NVP/|href=\"/$NVP/|g" || true
done

# Modify all links in VP that point to index.html to use absolute links ("/")
grep -Erl "href=\"(\.\./)*\.\.\"" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*\.\.\"|href=\"/\"|g" || true

# Change base URL to root in order to prevent asking for cookies consent in each version
grep -Erl "URL\(\"(\.\./)*\.\.\"" 3.0.0/docs | xargs sed -i "s|URL(\"\(\.\./\)*\.\.\"|URL(\"/\"|g" || true

BASE_URL="https://openvidu.io"
SITEMAP_FILE="sitemap.xml"
SITEMAP_INDEX="sitemap_index.xml"
SITEMAP="$BASE_URL/$VERSION/$SITEMAP_FILE.gz"
LASTMOD=$(date +%Y-%m-%d) # Current date

# Remove NVP in sitemap.xml
for NVP in "${NON_VERSIONED_PAGES[@]}"; do
    sed -i "\|<url>|{ :Loop N; \|</url>|! b Loop; \|$VERSION/$NVP|d }" "$VERSION/$SITEMAP_FILE"
done

# Regenerate sitemap.xml.gz
gzip -k -f "$VERSION/$SITEMAP_FILE"

# Create sitemap_index.xml if it doesn't exist
if [[ ! -f "$SITEMAP_INDEX" ]]; then
    echo "Index sitemap not found, creating new one..."
    cat <<EOF > "$SITEMAP_INDEX"
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</sitemapindex>
EOF
fi

# Check if the version is already included in sitemap_index.xml
if grep -q "<loc>$SITEMAP</loc>" "$SITEMAP_INDEX"; then
    echo "Version $VERSION already exists in sitemap_index.xml. Updating lastmod..."
    # Update lastmod of the version in sitemap_index.xml
    sed -i "\|<loc>$SITEMAP</loc>|!b;n;c\        <lastmod>$LASTMOD</lastmod>" "$SITEMAP_INDEX"
else
    echo "Adding new version $VERSION to sitemap_index.xml..."
    # Add new version to sitemap_index.xml after the <sitemapindex> tag
    sed -i "2a \    <sitemap>\n        <loc>$SITEMAP</loc>\n        <lastmod>$LASTMOD</lastmod>\n    </sitemap>" "$SITEMAP_INDEX"
fi

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
    rm "$VERSION/404.html"

    # Move redirect
    mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"

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
        grep -Erl "href=\"(\.\./)*$VP/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|href=\"\(\.\./\)*$VP/|href=\"/latest/$VP/|g" || true
    done

    # Remove version in the canonical tag of NVP
    grep -Erl "$VERSION/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|$VERSION/||g" || true

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

    # Move redirect
    mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"

    # Create root sitemap.xml
    # Create header of the sitemap.xml
    cat <<EOF > $SITEMAP_FILE
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>$BASE_URL/</loc>
        <lastmod>$LASTMOD</lastmod>
    </url>
EOF

    # Add NVP to the sitemap.xml
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        cat <<EOF >> $SITEMAP_FILE
    <url>
        <loc>$BASE_URL/$NVP/</loc>
        <lastmod>$LASTMOD</lastmod>
    </url>
EOF
    done

    # Close sitemap.xml
    echo "</urlset>" >> $SITEMAP_FILE

    # Generate sitemap.xml.gz
    gzip -k -f "$SITEMAP_FILE"

    SITEMAP="$BASE_URL/$SITEMAP_FILE.gz"
    # Check if the root sitemap is already included in sitemap_index.xml
    if grep -q "<loc>$SITEMAP</loc>" "$SITEMAP_INDEX"; then
        echo "Root sitemap already exists in sitemap_index.xml. Updating lastmod..."
        # Update lastmod of the root sitemap in sitemap_index.xml
        sed -i "\|<loc>$SITEMAP</loc>|!b;n;c\        <lastmod>$LASTMOD</lastmod>" "$SITEMAP_INDEX"
    else
        echo "Adding root sitemap to sitemap_index.xml..."
        # Add root sitemap to sitemap_index.xml before the </sitemapindex> tag
        sed -i "\|</sitemapindex>|i \    <sitemap>\n        <loc>$SITEMAP</loc>\n        <lastmod>$LASTMOD</lastmod>\n    </sitemap>" "$SITEMAP_INDEX"
    fi

    git add .
    git commit -am "Version $VERSION updated. Non-versioned pages updated"
fi

git push --set-upstream origin "$GH_BRANCH"

git checkout main

echo "Success publishing documentation for version $VERSION!"
