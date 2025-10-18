include .env

all: convert dev

convert:
	export NOTION_TOKEN=$(NOTION_TOKEN); \
	python py/notion_to_md.py --database_id $(NOTION_DB_ID) --post_path hugo-site/content/posts/

dev:
	hugo serve -D --bind 0.0.0.0 -s hugo-site

build:
	hugo build -s hugo-site

.PHONY: all convert dev build