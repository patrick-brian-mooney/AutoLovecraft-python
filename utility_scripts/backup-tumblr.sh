#!/bin/bash
# Back up Tumblr blog entries.
# Based partly on Mike Cramer's explanation and code: http://kiodane.tumblr.com/post/27508318036/wget-mirror-a-tumblr-site
OLDDIR=$(pwd)

DATETIME=$(date +%d%m%g%H%M%S)
cd /tmp
mkdir $DATETIME
cd $DATETIME

wget -mpNHk -D .media.tumblr.com,autolovecraft.tumblr.com -R "*avatar*","*\?*","*_[0-9][0-9][0-9].*" http://autolovecraft.tumblr.com -o /home/patrick/Desktop/autolovecraft-backup.log
tar c -PSvv --to-stdout * 2>> /home/patrick/Desktop/autolovecraft-backup.log | bzip2 -z 2>> /home/patrick/Desktop/autolovecraft-backup.log > "/lovecraft/backups/$DATETIME.tar.bz2"

cd ..
rm -R $DATETIME

cd $OLDDIR

echo
echo '#################'
echo "   WE'RE DONE"
echo '#################'
echo