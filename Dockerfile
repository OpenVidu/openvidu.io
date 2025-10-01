FROM squidfunk/mkdocs-material:9.6.20
RUN pip install mkdocs-glightbox mkdocs-llmstxt
ENTRYPOINT ["/sbin/tini", "--", "mkdocs"]
CMD ["serve", "--dirtyreload", "--dev-addr=0.0.0.0:8000"]