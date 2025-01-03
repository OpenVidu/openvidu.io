#!/bin/bash
set -e

# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

BASE_URL="https://openvidu.io"
GH_BRANCH="gh-pages"

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "conditions" "blog") # And root index.html and 404.html
VERSIONED_PAGES=("docs")

validateArgs() {
    # If there is no version passed to the script as an argument, exit
    if [ $# -lt 1 ]; then
        echo "Usage: $0 X.Y.Z"
        exit 1
    fi

    VERSION=$1
    UPDATE_LATEST=${2:-true}

    # Check if second argument is a boolean if provided
    if [ "$UPDATE_LATEST" != true && "$UPDATE_LATEST" != false ]; then
        echo "Second argument must be a boolean if provided: $0 X.Y.Z false"
        exit 1
    fi  
}

checkDependencies() {
    # Check if mike is installed
    command -v mike >/dev/null 2>&1 || {
        echo >&2 "mike not found. Install it with \"pip install mike\""
        exit 1
    }
}

checkGitStatus() {
    # Check if there are uncommitted changes in the repository
    if [[ $(git status --porcelain) ]]; then
        echo "There are uncommitted changes in the repository. Please commit or stash them before running this script"
        exit 1
    fi
}

prepareGitBranches() {
    # If branch gh-pages exists in the remote repository, pull changes
    if git ls-remote --heads origin "$GH_BRANCH" | grep -q "$GH_BRANCH"; then
        echo "Git branch '$GH_BRANCH' exists in the remote repository"
        git checkout "$GH_BRANCH"
        git pull origin "$GH_BRANCH"
        git checkout main
    else
        echo "Git branch '$GH_BRANCH' does not exist in the remote repository. This is the first version deployment"
    fi

    local VERSION_BRANCH="${VERSION}"
    # If the version branch exists in the remote repository, pull changes. If not, create it
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
}

deployVersion() {
    if [ "$UPDATE_LATEST" = true ]; then
        # Build and deploy the new version with mike, updating latest alias
        mike deploy --push --update-aliases "$VERSION" latest
        echo "New version $VERSION published with mike (latest alias updated to this new version)"
    else
        # Build and deploy the new version with mike
        mike deploy --push "$VERSION"
        echo "New version $VERSION published with mike (latest alias not updated)"
    fi
}

changeVersionedPagesLinks() {
    local ALL_PREFIXED_VP="${VERSIONED_PAGES[@]/#/$VERSION/}"

    # Change all links in VP that point to NVP to use absolute links ("/NVP/")
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        grep -Erl "href=\"(\.\./)*$NVP/" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*$NVP/|href=\"/$NVP/|g" || true
    done

    # Change all links in VP that point to index.html to use absolute links ("/")
    grep -Erl "href=\"(\.\./)*\.\.\"" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*\.\.\"|href=\"/\"|g" || true

    # Change base URL to root in order to prevent asking for cookies consent in each version
    grep -Erl "URL\(\"(\.\./)*\.\.\"" $ALL_PREFIXED_VP | xargs sed -i "s|URL(\"\(\.\./\)*\.\.\"|URL(\"/\"|g" || true
}

changeNonVersionedPagesLinks() {
    local ALL_PREFIXED_NVP="${NON_VERSIONED_PAGES[@]/#/$VERSION/}"

    # Remove version in all links of 404.html
    sed -i "s|/$VERSION/|/|g" "$VERSION/404.html"
    sed -i "s|\"/$VERSION\"|\"/\"|g" "$VERSION/404.html"

    for VP in "${VERSIONED_PAGES[@]}"; do
        sed -i "s|href=\"/$VP/|href=\"/latest/$VP/|g" "$VERSION/404.html"
    done

    # Change all links in NVP that point to VP to use absolute links to the latest version ("/latest/VP/")
    for VP in "${VERSIONED_PAGES[@]}"; do
        grep -Erl "href=\"(\.\./)*$VP/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|href=\"\(\.\./\)*$VP/|href=\"/latest/$VP/|g" || true
    done

    # Remove version in the canonical tag of NVP
    grep -Erl "$VERSION/" $ALL_PREFIXED_NVP "$VERSION/index.html" | xargs sed -i "s|$VERSION/||g" || true
}

updateIndexSitemap() {
    local SITEMAP_INDEX="sitemap_index.xml"
    local SITEMAP=$1
    local LASTMOD=$(date +%Y-%m-%d) # Current date

    # Create sitemap_index.xml if it doesn't exist
    if [[ ! -f "$SITEMAP_INDEX" ]]; then
        echo "Index sitemap not found, creating new one..."
        cat <<EOF > "$SITEMAP_INDEX"
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</sitemapindex>
EOF
    fi

    # Check if the sitemap is already included in sitemap_index.xml
    if grep -q "<loc>$SITEMAP</loc>" "$SITEMAP_INDEX"; then
        echo "Sitemap '$SITEMAP' already exists in $SITEMAP_INDEX. Updating lastmod..."
        # Update lastmod of the sitemap in sitemap_index.xml
        sed -i "\|<loc>$SITEMAP</loc>|!b;n;c\        <lastmod>$LASTMOD</lastmod>" "$SITEMAP_INDEX"
    else
        echo "Adding sitemap '$SITEMAP' to $SITEMAP_INDEX..."

        # If the sitemap include version, add it as the first sitemap. Otherwise, add it as the last one
        if [[ $SITEMAP == *"$VERSION"* ]]; then
            sed -i "2a \    <sitemap>\n        <loc>$SITEMAP</loc>\n        <lastmod>$LASTMOD</lastmod>\n    </sitemap>" "$SITEMAP_INDEX"
        else
            sed -i "\|</sitemapindex>|i \    <sitemap>\n        <loc>$SITEMAP</loc>\n        <lastmod>$LASTMOD</lastmod>\n    </sitemap>" "$SITEMAP_INDEX"
        fi
    fi
}

updateVersionSitemap() {
    local SITEMAP_FILE="sitemap.xml"

    # Remove NVP in sitemap.xml
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        sed -i "\|<url>|{ :Loop N; \|</url>|! b Loop; \|$VERSION/$NVP|d }" "$VERSION/$SITEMAP_FILE"
    done

    # Regenerate sitemap.xml.gz
    gzip -k -f "$VERSION/$SITEMAP_FILE"

    # Update sitemap_index.xml
    updateIndexSitemap "$BASE_URL/$VERSION/$SITEMAP_FILE.gz"
}

createRootSitemap() {
    local SITEMAP_FILE="sitemap.xml"
    local LASTMOD=$(date +%Y-%m-%d) # Current date

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

    # Update sitemap_index.xml
    updateIndexSitemap "$BASE_URL/$SITEMAP_FILE.gz"
}

changeSearchIndexLinks() {
    local SEARCH_INDEX="$VERSION/search/search_index.json"

    # Change all links to VP to use absolute links including the version ("/X.Y.Z/VP/")
    for VP in "${VERSIONED_PAGES[@]}"; do
        sed -i "s|\"location\":\"$VP/|\"location\":\"/$VERSION/$VP/|g" "$SEARCH_INDEX"
    done

    # Change all links to NVP to use absolute links ("/NVP/")
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        sed -i "s|\"location\":\"$NVP/|\"location\":\"/$NVP/|g" "$SEARCH_INDEX"
    done

    # Change all links to root to use absolute links ("/")
    sed -i "s|\"location\":\"\"|\"location\":\"/\"|g" "$SEARCH_INDEX"
}

copyFilesFromVersionToRoot() {
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
}

updateWebsite() {
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

    # Copy necessary file from main branch to gh-pages branch
    git restore --source main custom-versioning/redirect-from-version-to-getting-started.html || {
        echo 'Failure copying file from main branch'
        exit 1
    }

    # Wait until this file exists in gh-pages branch
    until [ -f ./custom-versioning/redirect-from-version-to-getting-started.html ]; do
        sleep 1
    done

    # Change versioned pages links in the new version
    changeVersionedPagesLinks

    # Change links in search_index.json to use absolute links in the new version
    changeSearchIndexLinks

    # Update sitemap.xml in the new version
    updateVersionSitemap

    if [ "$UPDATE_LATEST" = false ]; then
        echo "The latest version will not be updated"

        # Remove NVP from new version
        rm -rf "${VERSIONED_PAGES[@]/#/$VERSION/}"
        rm "$VERSION/404.html"

        # Move redirection file to the new version
        mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"

        # Commit the updated version folder
        git add .
        git commit -am "Version $VERSION updated. Non-versioned pages untouched"
    else
        echo "The latest version will be updated"

        # Change non-versioned pages links in the new version
        changeNonVersionedPagesLinks

        # Update root files with ones from the new version
        copyFilesFromVersionToRoot

        # Move redirection file to the new version
        mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"

        # Create root sitemap.xml
        createRootSitemap

        # Commit changes
        git add .
        git commit -am "Version $VERSION updated. Non-versioned pages updated"
    fi
    
    # Push changes
    git push --set-upstream origin "$GH_BRANCH"
    git checkout main
}

main() {
    validateArgs $@
    checkDependencies

    echo "Publishing new version $VERSION"

    # Navigate to the root of the repository based on the script location
    cd "$(dirname "$0")" || exit
    cd ..

    checkGitStatus
    prepareGitBranches
    deployVersion
    updateWebsite

    echo "Success publishing documentation for version $VERSION!"
}

main $@
