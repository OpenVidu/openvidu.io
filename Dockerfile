# Keep the tag in step with the mkdocs-material pin in publish-tool/pyproject.toml.
# `ovweb doctor --pins` fails when they disagree: a different theme version builds different
# markup, and the release-notes splice matches on that markup.
FROM squidfunk/mkdocs-material:9.8.0@sha256:dc3b5de76c6e30d18dc0922d4c4a7bed817e5e155f9ff0e594a53eb56e537e64
RUN pip install mkdocs==1.6.1 pymdown-extensions==12.1 mkdocs-glightbox==0.5.2 mkdocs-llmstxt==0.5.0 mkdocs-rss-plugin==1.19.0 pygments==2.21.0 gitpython==3.1.62 selectolax==0.4.11
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload", "--dirty"]
