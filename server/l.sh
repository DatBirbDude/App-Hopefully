#Reconfigure python3.6 to your binary name I think
echo "Ignore warning if first time running"
pkill python
rm nohup.out
echo "Hit ctrl-c once nohup gets rolling"
nohup python3.6 main.py &
echo "Now running main.py"
