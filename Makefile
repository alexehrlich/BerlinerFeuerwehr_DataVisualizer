all: setup

setup:
	@python3 -m venv venv && \
	source ./venv/bin/activate && \
	pip3 install -r requirements.txt

run:
	@source ./venv/bin/activate && \
	python3 bf_mission_count_viz.py

clean:
	@rm merged_mission_count_years.csv

fclean: clean
	@rm -rf ./venv
	
