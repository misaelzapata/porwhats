#!/usr/bin/env bash
pip install -r ./requirements.txt
chmod a+w /app/logs
supervisord -c /etc/supervisord.conf
