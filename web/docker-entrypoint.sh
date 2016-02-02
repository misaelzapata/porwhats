#!/usr/bin/env bash
pip install -r /app/requirements.txt
chmod a+w /app/logs
supervisord -c /etc/supervisord.conf
