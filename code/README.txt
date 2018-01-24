Getting up and running:


Connecting to Pyboard:
----------------------
- Plug the board into a USB port
- Open Device Manager and look for the device in the 'Ports' section
	- Identify which port is used (seems to be typically 'COM3')
- Run putty (search for putty.exe)
	- Under the Session tab, select connection type 'serial', enter the port name under Serial line (i.e. 'COM3'), and 115200 for the speed
	- Launch the session with 'open'
	
When the command line launches, it will automatically run any code that is stored on the pyboard in the main.py file


Updating the code:
------------------

