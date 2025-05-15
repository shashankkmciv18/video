Command to run celery
``` celery -A eventHandler.celery_app worker --loglevel=info -Q youtube,audio_queue```


Command to run flower

``` celery -A eventHandler.celery_app flower --port=8888```

Note: If you encounter permission issues with port 8888, you can try another port or use the `--address=127.0.0.1` option to bind only to localhost.

[//]: # ()
