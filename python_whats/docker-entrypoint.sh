#!/usr/bin/env bash
pip install -r requirements.txt
chmod a+w /app/logs
chmod a+w /root/.yowsup
supervisord -c /etc/supervisord.conf
