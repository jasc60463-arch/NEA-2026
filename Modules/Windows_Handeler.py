


def switch_desktop(index : int) -> bool:
    '''
    Switches to the virtual desktop to the given index.\n
    The index starts at 0 \n
    return False when failed
    '''
    import pyvda
    # if the desire virtual desktop doesn't exist
    if get_len_virual_desktops() < index:
        return False
    try:
        # move to desire virtual desktop
        desktops = pyvda.get_virtual_desktops()
        desktops[index].go()
        return True
    except IndexError as e:
        return False
    

def get_current_window() -> object | None:
    '''get the "appview" object of the current focused application  '''
    from pyvda import AppView
    try:
        return AppView.current()
    except:
        return None


def move_window_to_desktop(index : int, window = None) -> bool:
    '''
    Moves the current window to the virtual desktop with the given index.\n
    The index starts at 0\n
    When given a window (AppView object) it move the window instead
    return False when failed
    '''
    from pyvda import AppView, VirtualDesktop
    # if the desire virtual desktop doesn't exist
    if get_len_virual_desktops() < index:
        return False
    try:
        # if window is not empty
        if window:
            # move window to desire virtual desktop
            window.move(VirtualDesktop(index + 1))
        
        # if window is empty
        else:
            # move current focused window to desire virtual desktop
            AppView.current().move(VirtualDesktop(index + 1))
        return True
    
    except ValueError as e:
        return False


def start_application(app_name : str) -> bool:
    '''start an application, return False when failed'''
    import AppOpener
    try:
        AppOpener.open(app_name, output = True, match_closest = True, throw_error = True)
        return True
    except Exception as e:
        return False


def get_len_virual_desktops() -> int:
    '''return amount of virual desktop opened'''
    import pyvda
    return len(pyvda.get_virtual_desktops())


def pin() -> bool:
    '''pin the current application across all virtual desktop'''
    from pyvda import AppView
    try:
        AppView.current().pin()
        return True
    except Exception as e:
        return False

if __name__ == "__main__":

    exit()
    # import time
    # switch_desktop(1)  
    # time.sleep(2)
    # switch_desktop(0) 
    # AppView.current().pin()
    # AppView.current().move(VirtualDesktop(1))
    # move_current_window_to_desktop(1)
    # switch_desktop(1)
    # time.sleep(2)
    # move_current_window_to_desktop(0)
    # switch_desktop(0)
    # start_application('notepad')
    # start_application('chrome')
    # print(VirtualDesktop.create())
    # print(pyvda.get_virtual_desktops())
    # print(len(pyvda.get_virtual_desktops()))
    # print(VirtualDesktop.apps_by_z_order(VirtualDesktop.current()))
    # print(bring_window_to_foreground())

    # a = AppView.current()
    # print(AppView.current())
    # time.sleep(1)
    # AppView.set_focus(a)
    # print(move_window_to_desktop(0))
    # switch_desktop(0)