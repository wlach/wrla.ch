# Based on https://github.com/dherman/calculist/blob/master/Makefile

PUBLISHED_DIRS = blog feeds tags
PUBLISHED_FILES = sitemap.txt *.html

.PHONY: preview build publish

preview:
	raco frog -bp

build:
	raco frog -b

publish:
	rm -rf _build
	mkdir _build
	mv $(PUBLISHED_DIRS) $(PUBLISHED_FILES) _build/
	rm -rf $(PUBLISHED_DIRS)
	mv _build/* ./
	rmdir _build
	git add $(PUBLISHED_DIRS) $(PUBLISHED_FILES)
	git commit -a -m 'new post'

