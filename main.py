import file_handeling
import screens
import actions
import references


def main():
    # Logging setup
    logger = file_handeling.set_logger()
    if logger is None:
        return None
    
    logger.info('App Startup')

    # Load config
    cfg = file_handeling.get_config()
    # Load options
    options = references.get_options()
    # Set valid commands from options
    valid_cmds = sum(options.values(), [])

    try:
        # Main loop
        run = True
        while run is True:
            # Clear console and show header
            screens.print_header()

            # Show instructions
            screens.print_main_menu()

            # Set/Reset continue
            cont = ''

            # Get command
            cmd = input("\nEnter command: ")

            # Run command
            if cmd in options['search']:
                actions.setlist_search()

            # Exit and valid command checks
            if cmd in options['exit']:
                run = False
                break
            elif cont.lower() in options['exit']:
                run = False
                break
            elif cmd in valid_cmds:
                pass
            else:
                cont = input("Unknown command\nPress enter to continue ")

        logger.info("App exit")
    except Exception as e:
        logger.error(f"App crashed - {e}")
        logger.exception(f"Crash error")
        if cfg['testing'] is True:
            raise


if __name__ == '__main__':
    main()
