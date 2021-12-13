#!/usr/bin/env bash

cp /etc/rc.local /etc/rc.local.bak

cat<<EOF > /etc/rc.local
#!/usr/bin/env bash
sudo bash /bluetooth-keyboard-auto-loader/keyboard_config.sh
sudo chmod 777 /dev/hidg0
exit 0
EOF

chmod 755 /etc/rc.local