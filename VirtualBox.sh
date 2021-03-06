#!/bin/sh
BINFILE=$(basename "$0")
VBOXDIR=@LIBDIR@/VirtualBox

show_message() {
	if [ ! -z "$DISPLAY" ] && [ -x /usr/bin/gxmessage ]; then
		echo -e "$1" | gxmessage --center --buttons GTK_STOCK_OK -wrap -geometry 400x150 -name $BINFILE -file -
	else
		echo -e "$1"
	fi
}

if [ ! -d "$VBOXDIR" ]; then
	show_message "Can't find VirtualBox libraries! Can't continue!.\nCorrect this situation or contact with your system administrator."
	exit 1
fi

if [ ! -c /dev/vboxdrv ]; then
	show_message "Special character device /dev/vboxdrv doesn't exists!\nCheck your installation and whether vboxdrv kernel module is loaded."
	exit 1
fi

if [ ! -w /dev/vboxdrv ]; then
	show_message "You don't have write access to /dev/vboxdrv!\nCorrect this situation or contact with your system administrator."
	exit 1
fi

[ "$BINFILE" = "VBoxVRDP" ] && BINFILE="VBoxHeadless"

export LD_LIBRARY_PATH=$VBOXDIR
exec $VBOXDIR/$BINFILE ${1:+"$@"}
