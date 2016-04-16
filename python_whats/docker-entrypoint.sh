#!/usr/bin/env bash
pip install -r /python_whats/requirements.txt
chmod a+w /app/logs
supervisord -c /etc/supervisord.conf
