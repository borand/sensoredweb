nohup /home/andrzej/projects/sensoredweb/venv/bin/celery -A sensoredweb --workdir=/home/andrzej/projects/sensoredweb/ worker &
nohup /home/andrzej/projects/sensoredweb/venv/bin/celery -A sensoredweb --workdir=/home/andrzej/projects/sensoredweb/ beat &
nohup /home/andrzej/projects/sensoredweb/venv/bin/python /home/andrzej/projects/sensoredweb/manage.py runserver 0.0.0.0:8000 &

nohup /home/andrzej/venv/bin/python /home/andrzej/projects/ablib/ablib/hardware/i.py &