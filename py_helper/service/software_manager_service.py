class SoftwareManagerService:
	# Ubuntu Install package if doesn't exist

	"""
	PACKAGE_NAME="your_package_name"
	if dpkg -l | grep -q "^ii  $PACKAGE_NAME "; then
	    echo "$PACKAGE_NAME is installed."
	else
	    echo "$PACKAGE_NAME is not installed. Installing..."
	    sudo apt update
	    sudo apt install $PACKAGE_NAME
	fi

	"""
	pass