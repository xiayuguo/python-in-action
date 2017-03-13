#!/usr/bin/env bash

echo `date` "start celery" >> log/celery_service.log
nohup python celery_service.py > log/celery_service.log 2>&1 &

echo `date` "start app" >> log/app.log
nohup python app.py > log/app.log 2>&1 &