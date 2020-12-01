def start(_command_line_arguments):
	"""Starts the horizons. Will drop you to the main menu.
	@param _command_line_arguments: options object from optparse.OptionParser. see run_uh.py.
	"""
	global debug, preloader, command_line_arguments, gui, session
	command_line_arguments = _command_line_arguments
	# NOTE: globals are designwise the same thing as singletons. they don't look pretty.
	#       here, we only have globals that are either trivial, or only one instance may ever exist.

	from .engine import Fife

	# handle commandline globals
	debug = command_line_arguments.debug

	if command_line_arguments.restore_settings:
		# just delete the file, Settings ctor will create a new one
		os.remove(PATHS.USER_CONFIG_FILE)

	if command_line_arguments.mp_master:
		try:
			mpieces = command_line_arguments.mp_master.partition(':')
			NETWORK.SERVER_ADDRESS = mpieces[0]
			# only change port if port is specified
			if mpieces[2]:
				NETWORK.SERVER_PORT = parse_port(mpieces[2])
		except ValueError:
			print("Error: Invalid syntax in --mp-master commandline option. Port must be a number between 1 and 65535.")
			return False

	# init fife before mp_bind is parsed, since it's needed there
	horizons.globals.fife = Fife()

	if command_line_arguments.generate_minimap: # we've been called as subprocess to generate a map preview
		from horizons.gui.modules.singleplayermenu import generate_random_minimap
		generate_random_minimap(* json.loads(
		  command_line_arguments.generate_minimap
		  ))
		sys.exit(0)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		-[--->+<]>-.[---->+++++<]>-.+.++++++++++.++[->+++<]>.++++++++++.++++++++++.++[->+++<]>.++++++++.-[-->+<]>.--[--->++<]>--..-----------.+++++.-------.--------.+[->+++<]>+.[----->+<]>+.++++++.>-[----->+<]>.++++++[->++<]>.>-[----->+<]>.--[--->++<]>---.+.[-->+++++<]>-.[----->+<]>+.-------.
