from Scenarios import *


main_menu = True
while main_menu:
    main_menu = get_quit_event()
    left, right, down, up, space, shields, dampers, esc, pause = keystrokes()
    if esc:
        main_menu = False
    if space:
        # test()
        one_vs_one()
        pygame.time.delay(200)
    display_main_menu()

pygame.quit()

# TODO Guidance Property for Rockets
# TODO Inertial Damper Shield Variant
# TODO Anti-Gravity Obstacles (negative mass)
# TODO Black holes (suck in and spit out in random location)
# TODO Add Level Class
# TODO Change probabilities
# TODO Powerups on timer
# TODO Look into left side of screen
# TODO Set up test case to test aim under controlled situation
# TODO Add guided missile that goes fast
# TODO Damper that has a range
