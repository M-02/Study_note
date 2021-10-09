#!/bin/bash                                                        
Backup_dir="/backup"                                               
IP_info=$(hostname -i)                                             
# create backup dir                                                
mkdir -p $Backup_dir/$IP_info/                                     
                                                                   
#tar backup date                                                   
cd /                                                               
tar zchf $Backup_dir/$IP_info/system_backup_$(date +%F_week%w).tar.gz ./var/spool/cron/root ./etc/rc.local ./server/scripts ./etc/sysconfig/iptables                                                     
                                                                   
tar zchf $Backup_dir/$IP_info/www_backup_$(date +%F_week%w).tar.gz ./var/html/www                                                    
tar zchf $Backup_dir/$IP_info/www_log_backup_$(date +%F_week%w).tar.gz  ./app/logs                                                    
                                                                   
#del 7 day ago data                                                
find $Backup_dir -type f -mtime +7|xargs rm                        
                                                                   
#cerate finger file                                                
find $Backup_dir/ -type f -mtime -1 ! -name "finger*"|xargs md5sum >$Backup_dir/$IP_info/finger.txt                                   
                                                                   
#backup data info                                                  
rsync -avz $Backup_dir/ rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password                                          