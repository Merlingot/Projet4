# -------------------------------------------- #
#         Data acquisition script              #
# -------------------------------------------- #

# --------------------------------------------------------------- #
# This bash script acquires the distorted fringes from original   #
# fringes in order to make surface cartography with codedlight    #
# library                                                         #
#                                                                 #
# Usage:           bash acquire.sh {make_arg}                     #
# --------------------------------------------------------------- #

## Function definition

save_Thrash(){
	
	local found="false"
	local i=0
	while [ $found = "false" ]
	do	
		if [ ! -d "./archive/scan_$1_3channels_$i" ]; then
			mv "./scan_$1_3channels" "./archive/scan_$1_3channels_$i"
			found="true"
		else
			i=$(($i+1))
		fi
	done
}


manage_folders(){
	if [ ! -d "scan_$1_3channels" ]; then
		mkdir "scan_$1_3channels"
	else
		if [ ! -z "$(ls -A ./scan_$1_3channels)" ]; then
			save_Thrash $1
			mkdir "scan_$1_3channels"
		fi
	fi
}

take_photo(){
	echo $1
}



#################################################################
## Main

# Managing old folders
manage_folders "AV"
manage_folders "PG"

# Acquiring loop

i=0
fringes="./fringes/*.png"
for fringe in $fringes
do
	# Show pictures
	eog --single-window -f $fringe &
	sleep 5
	
	# Taking photo
	i=$(($i+1))
	take_photo $i
done

./unwrap.sh

