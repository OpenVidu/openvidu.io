# Keep the tag in step with the mkdocs-material pin in publish-tool/pyproject.toml.
# `ovweb doctor --pins` fails when they disagree: a different theme version builds different
# markup, and the release-notes splice matches on that markup.
FROM squidfunk/mkdocs-material:9.7.6
RUN pip install mkdocs-glightbox mkdocs-llmstxt mkdocs-rss-plugin
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload", "--dirtyreload"]
