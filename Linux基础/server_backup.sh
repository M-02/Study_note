#!/bin/bash                                                            
# del 180 ago data                                                     
find /backup/ -type f -mtime +180 ! -name "*week1.tar.gz"|xargs rm     
                                                                       
#check data                                                            
find /backup/ -type f -name "finger.txt"|xargs md5sum -c >/tmp/check.txt                                                                      
#send chech mail                                                       
mail -s "check back info for $(date +%F)" 1723433302@qq.com </tmp/check.txt                                                                   