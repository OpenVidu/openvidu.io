#!/bin/bash
set -e

# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

GH_BRANCH="gh-pages"

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "openvidu-meet-vs-openvidu-platform" "conditions" "blog" "about-us" "research" "acknowledgments") # And root index.html, 404.html, robots.txt, llms.txt and llms-full.txt
VERSIONED_PAGES=("docs" "meet")

validateArgs() {
    # If there is no version passed to the script as an argument, exit
    if [ $# -lt 1 ]; then
        echo "Usage: $0 X.Y"
        exit 1
    fi

    VERSION=$1
    UPDATE_LATEST=${2:-true}

    # Check if second argument is a boolean if provided
    if [ "$UPDATE_LATEST" != true ] && [ "$UPDATE_LATEST" != false ]; then
        echo "Second argument must be a boolean if provided: $0 X.Y false"
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
    grep -Erl "URL\(\"(\.\./)*\.\.\",location\)" $ALL_PREFIXED_VP | xargs sed -i "s|URL(\"\(\.\./\)*\.\.\",location)|URL(\"/\",location)|g" || true
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

    # Remove the version prefix from the self-referencing URLs the theme generates for each
    # non-versioned page (the <link rel="canonical">, the og:url meta and the JSON-LD
    # @id/url/mainEntityOfPage): these pages are built under the version folder but served
    # from the site root, so their own URL must not carry the version.
    #
    # Author-written, version-pinned links to versioned pages (/X.Y/docs/, /X.Y/meet/) — used
    # e.g. by release-notes links in blog posts — MUST be preserved. A plain "s|$VERSION/||g"
    # would strip the version out of them too, silently breaking those links. So the versioned
    # links are shielded with a sentinel while the version is stripped, then restored.
    for FILE in $(grep -Erl "/$VERSION/" $ALL_PREFIXED_NVP "$VERSION/index.html" || true); do
        for VP in "${VERSIONED_PAGES[@]}"; do
            sed -i "s|/$VERSION/$VP/|/@@KEEPVERSION@@/$VP/|g" "$FILE"
        done
        sed -i "s|/$VERSION/|/|g" "$FILE"
        sed -i "s|/@@KEEPVERSION@@/|/$VERSION/|g" "$FILE"
    done

    # Update llms.txt links
    # Replace version with 'latest' for versioned pages
    for VP in "${VERSIONED_PAGES[@]}"; do
        sed -i "s|/$VERSION/$VP/|/latest/$VP/|g" "$VERSION/llms.txt"
    done
    
    # Remove version from non-versioned pages
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        sed -i "s|/$VERSION/$NVP/|/$NVP/|g" "$VERSION/llms.txt"
    done
    
    # Remove version from root URL
    sed -i "s|/$VERSION/index.md|/index.md|g" "$VERSION/llms.txt"

    RSS_FILES=("feed_rss_created.xml" "feed_rss_updated.xml" "feed_json_created.json" "feed_json_updated.json")
    for RSS_FILE in "${RSS_FILES[@]}"; do
        # Remove version in RSS feed xmls
        sed -i "s|/$VERSION/|/|g" "$VERSION/$RSS_FILE"
    done
}

changeSearchIndexLinks() {
    local SEARCH_INDEX="$VERSION/search/search_index.json"

    # Change all links to VP to use absolute links including the version ("/X.Y/VP/")
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

updateSitemap() {
    local SITEMAP_FILE="sitemap.xml"
    
    # Copy sitemap from version folder to root, replacing any existing one
    cp "$VERSION/$SITEMAP_FILE" .
    
    echo "Updating sitemap URLs..."
    
    # Replace version with 'latest' for versioned pages
    for VP in "${VERSIONED_PAGES[@]}"; do
        sed -i "s|/$VERSION/$VP/|/latest/$VP/|g" "$SITEMAP_FILE"
    done
    
    # Remove version from non-versioned pages
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        sed -i "s|/$VERSION/$NVP/|/$NVP/|g" "$SITEMAP_FILE"
    done
    
    # Remove version from root URL
    sed -i "s|/$VERSION/</loc>|/</loc>|g" "$SITEMAP_FILE"
    
    # Generate compressed sitemap
    gzip -k -f "$SITEMAP_FILE"
    
    echo "Sitemap updated successfully"
}

updateVersionSitemap() {
    local SITEMAP_FILE="sitemap.xml"

    # Remove NVP in sitemap.xml
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        sed -i "\|<url>|{ :Loop N; \|</url>|! b Loop; \|$VERSION/$NVP|d }" "$VERSION/$SITEMAP_FILE"
    done

    # Regenerate sitemap.xml.gz
    gzip -k -f "$VERSION/$SITEMAP_FILE"
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
    mv "$VERSION/index.md" . # Home page
    mv "$VERSION/404.html" . # 404 page
    mv "$VERSION/robots.txt" . # robots.txt
    mv "$VERSION/llms.txt" . # LLMs list
    mv "$VERSION/llms-full.txt" . # Full LLMs list
    mv "$VERSION/feed_rss_created.xml" . # RSS feed
    mv "$VERSION/feed_rss_updated.xml" . # RSS feed
    mv "$VERSION/feed_json_created.json" . # RSS feed
    mv "$VERSION/feed_json_updated.json" . # RSS feed
    mv "$VERSION/rss.xsl" . # RSS feed


    for NVP in "${NON_VERSIONED_PAGES[@]}"; do # Other NVP
        # Delete previous root version of the page
        rm -rf "$NVP"
        # Move new page as their root version
        mv "$VERSION/$NVP" .
    done
}

copyReleasesFromTo() {
    # Copy the releases pages (Meet and Platform) from a SOURCE version folder into a
    # DESTINATION version folder, so the destination shows the full, most-recent release
    # notes regardless of the documentation version being browsed.
    #
    # The release notes' own links are authored as absolute, version-pinned URLs, so the
    # only relative links left in the built page are theme chrome (navigation menu and
    # hashed assets). Those are rewritten in the copy to absolute "/latest/" links, because
    # an older destination folder does not contain the same hashed asset files nor every
    # page the latest nav points at. The canonical tag is intentionally left untouched: the
    # copy already declares the source (latest) version as canonical, which consolidates
    # every copy onto a single URL.
    local SRC="$1" # source version folder (holds the most recent release notes)
    local DST="$2" # destination version folder

    # Never copy a version onto itself (it would rewrite the canonical page's own links)
    if [ "$SRC" = "$DST" ]; then
        return 0
    fi

    for VP in "${VERSIONED_PAGES[@]}"; do
        local SRC_DIR="$SRC/$VP/releases"
        local DST_DIR="$DST/$VP/releases"

        # Only copy when both sides have this versioned releases page
        # (e.g. Meet documentation did not exist before 3.4.0)
        [ -f "$SRC_DIR/index.html" ] || continue
        [ -d "$DST_DIR" ] || continue

        # HTML version (always generated). The release notes' own links are authored as
        # absolute, version-pinned URLs, so the only relative links left in the built page
        # are theme-generated: the navigation menu and the hashed CSS/JS/image assets. They
        # still must be rewritten to "/latest/" (the page sits two levels deep, so "../../"
        # is the version root and "../" the <vp> root; longer pattern first), because the
        # assets carry per-build content hashes and the nav reflects the latest structure,
        # so left relative they would break styling or 404 against pages an older folder
        # never had. Only href/src attributes are touched, so Material's runtime JS config
        # (base, search path) keeps working per version folder; <link rel="canonical"> is
        # left as-is.
        cp "$SRC_DIR/index.html" "$DST_DIR/index.html"
        sed -i -E "s#(href|src)=\"\.\./\.\./#\1=\"/latest/#g" "$DST_DIR/index.html"
        sed -i -E "s#(href|src)=\"\.\./#\1=\"/latest/$VP/#g" "$DST_DIR/index.html"
        echo "Copied releases page into '$DST_DIR/index.html' (internal links pointing to /latest/)"

        # Markdown version for LLMs. The mkdocs-llmstxt plugin generates it for pages listed
        # in its 'sections' (both releases pages are). It may still be absent for versions
        # built before the page was added there, so its presence is checked. Its internal
        # links are already absolute URLs emitted by the plugin, so it is copied verbatim
        # with no rewriting.
        if [ -f "$SRC_DIR/index.md" ]; then
            cp "$SRC_DIR/index.md" "$DST_DIR/index.md"
            echo "Copied releases Markdown (llms) into '$DST_DIR/index.md'"
        fi
    done
}

copyReleasesToAllOtherVersions() {
    # Copy the just-published latest release notes into every other published version folder.
    if [ ! -f versions.json ]; then
        echo "versions.json not found; skipping copy of releases to other versions"
        return 0
    fi

    local ALL_VERSIONS
    ALL_VERSIONS=$(grep -oE "\"version\"[[:space:]]*:[[:space:]]*\"[^\"]+\"" versions.json | sed -E "s/.*\"([^\"]+)\"$/\1/")

    for V in $ALL_VERSIONS; do
        copyReleasesFromTo "$VERSION" "$V"
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

    # Copy necessary file from appropriate branch to gh-pages branch
    if [ "$UPDATE_LATEST" = true ]; then
        # Get file from main branch for latest version
        SOURCE_BRANCH="main"
    else
        # Get file from version branch for past version updates
        SOURCE_BRANCH="$VERSION"
    fi
    
    git restore --source "$SOURCE_BRANCH" custom-versioning/redirect-from-version-to-getting-started.html || {
        echo "Failure copying file from $SOURCE_BRANCH branch"
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

    if [ "$UPDATE_LATEST" = false ]; then
        echo "The latest version will not be updated"

        # Remove NVP from new version. All removals are tolerant ("|| true") because old
        # version branches may not generate some of these files at all (e.g. llms.txt and
        # the RSS feeds require plugins that older mkdocs.yml configurations do not have)
        rm -rf "${NON_VERSIONED_PAGES[@]/#/$VERSION/}"
        rm "$VERSION/404.html" || true
        rm "$VERSION/index.md" || true
        rm "$VERSION/robots.txt" || true
        rm "$VERSION/llms.txt" || true
        rm "$VERSION/llms-full.txt" || true
        rm "$VERSION/feed_rss_created.xml" || true # RSS feed
        rm "$VERSION/feed_rss_updated.xml" || true # RSS feed
        rm "$VERSION/feed_json_created.json" || true # RSS feed
        rm "$VERSION/feed_json_updated.json" || true # RSS feed
        rm "$VERSION/rss.xsl" || true # RSS feed

        # Move redirection file to the new version
        mv custom-versioning/redirect-from-version-to-getting-started.html "$VERSION/index.html"

        # Update sitemap in the new version removing NVP
        updateVersionSitemap

        # This is a past version: overwrite its just-rebuilt releases pages with the current
        # latest ones, so it still shows the full, most-recent release notes
        LATEST_VERSION=$(readlink latest 2>/dev/null || true)
        if [ -n "$LATEST_VERSION" ]; then
            copyReleasesFromTo "$LATEST_VERSION" "$VERSION"
        else
            echo "Could not resolve the 'latest' symlink; releases pages left as built"
        fi

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

        # Update sitemap.xml
        updateSitemap

        # Update sitemap in the new version removing NVP
        updateVersionSitemap

        # Copy the newly published latest release notes into every other version folder, so
        # a user browsing any documentation version sees the full, most-recent release notes
        copyReleasesToAllOtherVersions

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
