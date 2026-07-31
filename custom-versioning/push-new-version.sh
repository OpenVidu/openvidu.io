#!/bin/bash
set -e

# This script builds and pushes a new version of the documentation
# It updates the non-versioned pages of the documentation

GH_BRANCH="gh-pages"

ASSETS=("assets" "javascripts" "stylesheets" "search")
NON_VERSIONED_PAGES=("account" "pricing" "support" "openvidu-meet-vs-openvidu-platform" "openvidu-vs-livekit" "openvidu-vs-mediasoup" "conditions" "blog" "about-us" "research" "acknowledgments") # And root index.html, 404.html, robots.txt, llms.txt and llms-full.txt
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

    # Check if python3 is available (used by copy-releases-content.py). It always is in
    # practice, since mkdocs and mike are Python tools, but the failure would otherwise
    # surface halfway through a publish
    command -v python3 >/dev/null 2>&1 || {
        echo >&2 "python3 not found. It is required to copy the releases pages content"
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

    # Pin raw-HTML asset references in versioned pages to this version's own asset folders.
    # Authors write root-absolute asset refs in raw HTML blocks (src="/assets/...", see the
    # README "Link rules": MkDocs does not process raw HTML, so a relative path would need a
    # fragile per-page "../" depth, impossible to get right in shared snippets). At runtime,
    # the root /assets/ folder always holds the LATEST publish's assets (they are copied to
    # root by copyFilesFromVersionToRoot), so a versioned page must reference /X.Y/assets/
    # instead: its assets may change or disappear in later versions. Markdown asset links
    # need no pinning: MkDocs already rewrites them at build time into relative URLs that
    # stay inside the version folder.
    for ASSET_DIR in "assets" "javascripts" "stylesheets"; do
        grep -Erl "(src|href)=\"/$ASSET_DIR/" $ALL_PREFIXED_VP | xargs sed -i -E "s#(src|href)=\"/$ASSET_DIR/#\1=\"/$VERSION/$ASSET_DIR/#g" || true
    done

    # Change all links in VP that point to NVP to use absolute links ("/NVP/")
    for NVP in "${NON_VERSIONED_PAGES[@]}"; do
        grep -Erl "href=\"(\.\./)*$NVP/" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*$NVP/|href=\"/$NVP/|g" || true
    done

    # Change all links in VP that point to index.html to use absolute links ("/")
    grep -Erl "href=\"(\.\./)*\.\.\"" $ALL_PREFIXED_VP | xargs sed -i "s|href=\"\(\.\./\)*\.\.\"|href=\"/\"|g" || true

    # Change base URL to root in order to prevent asking for cookies consent in each version
    grep -Erl "URL\(\"(\.\./)*\.\.\",location\)" $ALL_PREFIXED_VP | xargs sed -i "s|URL(\"\(\.\./\)*\.\.\",location)|URL(\"/\",location)|g" || true

    # Point each versioned page's self-referencing SEO URLs (canonical, og:url) at the
    # stable /latest/ alias instead of this version number, so ranking signals consolidate
    # on one evergreen URL across releases instead of churning every release (issue #1).
    # These two tags are the only ones that carry page.canonical_url for versioned pages:
    # the JSON-LD emitted for docs/index.md and meet/index.md already hardcodes /latest/
    # (see docs/overrides/partials/json-ld.html), and no other versioned page emits JSON-LD
    # at all. NOTE: only these SEO tags are touched — the /$VERSION/assets/ pins applied
    # above, and any author-pinned /X.Y/... links elsewhere on the page, are left untouched.
    for FILE in $(grep -Erl 'rel="canonical"|property="og:url"' $ALL_PREFIXED_VP || true); do
        sed -i -E "s#(rel=\"canonical\" href=\"https://openvidu.io)/$VERSION/#\1/latest/#g" "$FILE"
        sed -i -E "s#(property=\"og:url\" content=\"https://openvidu.io)/$VERSION/#\1/latest/#g" "$FILE"
    done
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
    # Copy the *content* of the releases pages (Meet and Platform) from a SOURCE version
    # folder into a DESTINATION version folder, so the destination shows the full,
    # most-recent release notes regardless of the documentation version being browsed.
    #
    # Only the release notes body and the table of contents travel. Everything else in the
    # destination page is left exactly as that version built it: header, tabs, navigation
    # menu, footer, canonical URL, asset URLs and Material's runtime config all keep
    # pointing inside the destination version. This is what keeps a visitor who opens
    # /3.4/docs/releases/ browsing the 3.4 documentation (and what makes the outdated-version
    # banner show up there, like on any other page of an old version).
    #
    # The splice itself is done by copy-releases-content.py: the table of contents nests one
    # <nav> per heading level, so finding where a region ends needs tag-depth counting, which
    # sed cannot do. See that script for the regions and the guarantees it checks.
    local SRC="$1" # source version folder (holds the most recent release notes)
    local DST="$2" # destination version folder
    local STATUS

    # Never copy a version onto itself
    if [ "$SRC" = "$DST" ]; then
        return 0
    fi

    for VP in "${VERSIONED_PAGES[@]}"; do
        local SRC_DIR="$SRC/$VP/releases"
        local DST_DIR="$DST/$VP/releases"

        # Only copy when both sides have this versioned releases page
        # (e.g. Meet documentation did not exist before 3.4.0)
        [ -f "$SRC_DIR/index.html" ] || continue
        [ -f "$DST_DIR/index.html" ] || continue

        # Exit code 2 means the destination page did not expose the expected regions (an old
        # version folder may have been built by a different theme version): warn loudly and
        # leave that page as built, rather than aborting a publish that is already half done.
        # Any other non-zero exit is a genuine problem with the source page and aborts the
        # publish through "set -e".
        STATUS=0
        python3 "$RELEASES_CONTENT_HELPER" "$SRC_DIR/index.html" "$DST_DIR/index.html" || STATUS=$?
        if [ "$STATUS" -eq 2 ]; then
            echo "WARNING: could not splice the releases content into '$DST_DIR/index.html'; left as built"
        elif [ "$STATUS" -ne 0 ]; then
            return "$STATUS"
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

stageReleasesContentHelper() {
    # copy-releases-content.py is used from updateWebsite, which runs with the gh-pages
    # branch checked out. This folder does not exist on gh-pages, so by then the file would
    # be gone from the working tree (this very script only survives because bash keeps its
    # file descriptor open). Stage a copy outside the working tree while it is still there.
    # It must not simply be restored into the gh-pages working tree: updateWebsite runs
    # "git add ." and would publish it as part of the website.
    RELEASES_CONTENT_HELPER="$(mktemp)"
    trap 'rm -f "$RELEASES_CONTENT_HELPER"' EXIT
    cp custom-versioning/copy-releases-content.py "$RELEASES_CONTENT_HELPER"
}

main() {
    validateArgs $@
    checkDependencies

    echo "Publishing new version $VERSION"

    # Navigate to the root of the repository based on the script location
    cd "$(dirname "$0")" || exit
    cd ..

    stageReleasesContentHelper
    checkGitStatus
    prepareGitBranches
    deployVersion
    updateWebsite

    echo "Success publishing documentation for version $VERSION!"
}

main $@
