nohup /home/andrzej/projects/sensoredweb/venv/bin/celery -A sensoredweb --workdir=/home/andrzej/projects/sensoredweb/ worker &
nohup /home/andrzej/projects/sensoredweb/venv/bin/celery -A sensoredweb --workdir=/home/andrzej/projects/sensoredweb/ beat &
nohup /home/andrzej/projects/sensoredweb/venv/bin/python /home/andrzej/projects/sensoredweb/manage.py runserver 0.0.0.0:8000 &
nohup /home/andrzej/venv/bin/python /home/andrzej/projects/ablib/ablib/hardware/sermon.py run --dev=/dev/ttyUSB2 > /dev/null &
nohup /home/andrzej/venv/bin/python /home/andrzej/projects/ablib/ablib/hardware/sermon.py run --dev=/dev/arduino > /dev/null &
nohup /home/andrzej/venv/bin/python /home/andrzej/projects/ablib/ablib/hardware/insteon.py > /dev/null &
nohup /home/andrzej/venv/bin/python /home/andrzej/projects/realtime/rtweb/rtweb.py > /dev/null &
nohup /home/andrzej/venv/bin/python /home/andrzej/projects/ulog/server/ulogserver.py -port 8889 > /dev/null &
nohup /home/andrzej/venv/bin/celery -A datastore --workdir=/home/andrzej/projects/ablib/ablib/daq worker --loglevel=info > /dev/null &


