FROM squidfunk/mkdocs-material:9.7.1
RUN pip install mkdocs-glightbox mkdocs-llmstxt mkdocs-rss-plugin
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000", "--livereload", "--dirtyreload"]