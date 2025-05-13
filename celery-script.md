Command to run celery
``` celery -A eventHandler.celery_app worker --loglevel=info -Q youtube,audio_queue```


Command to run flower

``` celery -A eventHandler.celery_app flower --port=5555```

