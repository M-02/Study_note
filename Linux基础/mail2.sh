#!/usr/bin
read -p "输入你的邮件地址:" m1

read -p "输入你的邮件密码:" password
yum install -y mailx
mkdir -p /root/.certs
echo "# mail config
set from=$m1
set smtp=smtps://smtp.163.com:465  
set smtp-auth-user=$m1
set smtp-auth-password=$password 
set smtp-auth=login 
set nss-config-dir=/root/.certs  
set ssl-verify=ignore " >>/etc/mail.rc
echo -n | openssl s_client -connect smtp.163.com:465 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > ~/.certs/163.crt
certutil -A -n "GeoTrust SSL CA" -t "C,," -d ~/.certs -i ~/.certs/163.crt
certutil -A -n "GeoTrust Global CA" -t "C,," -d ~/.certs -i ~/.certs/163.crt
cd /root/.certs/
certutil -A -n "GeoTrust SSL CA - G3" -t "Pu,Pu,Pu" -d ./ -i 163.crt
read -p "输入你想发送的收件人:" m2
read -p "输入你想发送的信息:" ms
echo $ms | mail -v -s "this is Test Mail" $m2