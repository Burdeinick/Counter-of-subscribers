build :
	python3 Application/testing/preparing_db.py

droptables :
	python3 Application/testing/drop_tables.py

test :
	python3 Application/testing/test_logic.py

run :
	python3 Application/main.py

addgroup :
	python3 Application/scripts/logic/add_new_group.py

