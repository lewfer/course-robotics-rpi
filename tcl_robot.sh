DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Think Create Learn Robot service started at ${DATE}" | systemd-cat -p info

cd /home/pi/tcl
python3 robot.py
