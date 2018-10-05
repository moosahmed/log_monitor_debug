#!/usr/bin/env bash

# Find the average number of messages per hour for a 24 hour period not including the last 10 hours, so 34 hours ago - 10 hours ago
cat /var/log/kern.log | awk -v start_date="$(date --date="34 hours ago" +"%b %d %T")" -v end_date="$(date --date="10 hours ago" +"%b %d %T")" '$1FS$2FS$3>start_date && $1FS$2FS$3<end_date {print}' | awk 'END{print NR/24}'

# Find the average number of messages per hour for the last 12 hours. Messages should contain wlp2s0 in the first 6 letters of the 7th word
cat /var/log/kern.log | awk 'substr($7,1,6)=="wlp2s0" {print}' | awk -v start_date="$(date --date="12 hours ago" +"%b %d %T")" '$1FS$2$3>start_date {print}' | awk 'END{print NR/12}'

# Find the busiest minute in the last 48 hours (which minute of a particular day had the most messages for that minute)
cat /var/log/kern.log | awk -v start_date="$(date --date="48 hours ago" +"%b %d %T")" '$1FS$2$3>start_date {print}' | cut -c-12 | uniq -c | sort -nr | head -1
