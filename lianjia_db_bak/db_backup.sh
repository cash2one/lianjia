#!/bin/bash
current_date=$(date +%Y%m%d)
mysqldump -ulianjia_user -pJN7lebwqHhwCtYGq -hrdsdld66mt04nt1lt3k5o.mysql.rds.aliyuncs.com lianjia_db > lianjia_db.sql_"$current_date"
