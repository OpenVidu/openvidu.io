# Keep the tag in step with the zensical pin in publish-tool/pyproject.toml.
# `ovweb doctor --pins` fails when they disagree: a different Zensical version builds different
# markup, and the release-notes splice matches on that markup.
FROM zensical/zensical:0.0.68@sha256:862eb2099df9c20e4821e54cfc442a206fadb72bf6e8171645bc8a1dfb588ffd
# ovweb: the build loads its Markdown extensions by name (mkdocs.yml, markdown_extensions). Its
# pins ([validate]) are the ones the base image already carries. The checkout mounted at /docs
# takes precedence over the installed copy, so an edit to publish-tool/src/ovweb/mdx/ is live.
COPY publish-tool /tmp/publish-tool
RUN pip install --no-cache-dir "/tmp/publish-tool[validate]" && rm -rf /tmp/publish-tool
ENV PYTHONPATH=/docs/publish-tool/src
ENTRYPOINT ["/sbin/tini", "--", "zensical"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
