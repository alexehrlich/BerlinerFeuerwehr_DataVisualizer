all: setup run

setup:
	@python3 -m venv venv && \
	. ./venv/bin/activate && \
	pip3 install -r requirements.txt

run:
	@. ./venv/bin/activate && \
	python3 bf_mission_count_viz.py

fetch_data:
	@rm -f merged_mission_count_years.csv
	@$(MAKE) run

fclean:
	@rm -rf ./venv
	@rm -f merged_mission_count_years.csv
