#!/usr/bin/env bash

# get the count of the name "allen" "mark" and "tim" from names.log - not case sensitive.

cat names.log | tr "[:upper:]" "[:lower:]" | tr -s ' ' '\n' | sort | uniq -c | sort -nr | egrep 'mark|tim|allen' | awk '{print $2FS"appears",$1,"times"}'

# one awk command with if statement looking for name ==
awk '{ for (i=1;i<=NF;i++) count[ tolower( $i ) ]++} END{ for ( name in count ) { if (name == "tim" || name == "allen" || name == "mark") {print name " appears " count[ name ] " times" ;}}}' names.log

# one awk command setting up array first then looking in array for if statement
awk 'BEGIN{names["tim"] names["allen"] names["mark"]} { for (i=1;i<=NF;i++) count[ tolower( $i ) ]++} END{ for ( name in count ) { if (name in names) {print name " appears " count[ name ] " times" ;}}}' names.log