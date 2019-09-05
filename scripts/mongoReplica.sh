#!/bin/bash


# if [ ! -d remote ];
# 	then
# 		mkdir remote
# 	else
# 		diskutil umount force remote
# fi

sshfs ubuntu@ec2-52-74-149-82.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/ remote -f -o cache_timeout=1 -o IdentityFile=/Users/abhishek/test.pem

# sshfs ubuntu@ec2-52-76-147-74.ap-southeast-1.compute.amazonaws.com:/home/ubuntu/ remote -o IdentityFile=/Users/abhishek/test-daybox.pem

cd remote
echo `ls`

# cd ../
# diskutil umount force remote