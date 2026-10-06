import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
from kivy.config import Config

from Modules import *
from datetime import datetime
from pyautogui import position as mouse_position

import time
import threading
import keyboard
import json
import os



def get_time() -> str:
    '''get the current time (Hour:Minutes:Seconds) and return as a string'''
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_date() -> str:
    '''get the current date (Year:Month:Day) and return as a string'''
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


class Welcome_Frame(Screen):
    '''The Class that handels the logic of the Welcome page'''
    ...


class Main_Page_Frame(Screen):
    '''The Class that handels the logic of the Menu'''
    ...
    

class File_Sorter_Frame(Screen):
    '''The Class that handels the logic of the File Sorter menu'''
    
    # create a properties that can be accessed through .kv file and every other places
    destination_path = StringProperty('')
    source_path = StringProperty('')

    # decleare variable filter type
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_type = ""
        
    # called when the button "source file" in kivy is clicked
    def select_source_folder(self) -> None:
        # import function plyer to open the directory for the user to choose the file path 
        # when selected call the method selected_source and pass the path selected as parameter  
        from plyer import filechooser
        filechooser.choose_dir(on_selection = self.selected_source) 

    # called when user choose a path in the filechooser
    def selected_source(self, selection : str) -> None:
        # check if selection is empty
        if selection:
            # if selection is not empty assign self.source_path to the path given in parameter 
            self.source_path = str(selection[0])
        else:
            # if selection is empty then assign self.source_path to an empty string
            self.source_path = ''

    # called when the button "destination file" in kivy is clicked
    def select_destination_folder(self) -> None:
        # import function plyer to open the directory for the user to choose the file path
        # when selected call the method selected_destination and pass the path selected as parameter  
        from plyer import filechooser
        filechooser.choose_dir(on_selection = self.selected_destination) 

    # called when user choose a path in the filechooser
    def selected_destination(self, selection) -> None:
        # check if selection is empty
        if selection:
            # if selection is not empty assign self.destination_path to the path given in parameter 
            self.destination_path = str(selection[0])
        else:
            # if selection is empty then assign self.destination_path to an empty string
            self.destination_path = ''

    # called when the user selected an option from the spinner and return the text of the option as parameter
    def on_spinner_select(self, text : str) -> None:
        self.filter_type = text.replace('\n', '')

    # called when the "copy file" button is clicked check if all selected arguments are valid to apply
    def execution_validation(self) -> None:
        # check if filter type is empty
        if self.filter_type == "":
            # if it is empty create a pop up screen warning the user
            popup = Popup_Frame(title = "No filter type selected",
                                text = "Please select a filter type before executing the file sorting.",
                                confirmation = False)
            popup.open()
            return
        
        # check if the source path and destination path is valid
        if os.path.exists(self.source_path) and os.path.exists(self.destination_path):
            # if it is valid create a pop up screen to confirm the action
            popup = Popup_Frame(title = "Confirmation", 
                                text = f"Are you sure you want to sort the files in \n{self.source_path}\nand copy them to \n{self.destination_path} ?", 
                                confirmation = True,
                                confirmed_callback = self.sort_file)
        else:
            # if it is not valid create a pop up screen warning the user
            popup = Popup_Frame(title = "Invalid Paths",
                                text = "The destination path or source path doesn't exist.\nPlease select a valid path.",
                                confirmation = False)
        popup.open()


    def sort_file(self) -> None:
        '''sorting and transfer files'''
        # store all exisitng folder in a global vairable and later to be used
        check_existing_folders(self.destination_path)
        # get all the files in the source path
        files = get_items(self.source_path)
        try:
            # check the filter type
            # then sort and transfer file based on the sorting method 
            match self.filter_type:
                case "Sort by creation date":
                    transfer_files(files, Source_path = self.source_path, Destination_path = self.destination_path, sort = "C_Date")
                case "Sort by last edit":
                    transfer_files(files, Source_path = self.source_path, Destination_path = self.destination_path, sort = "M_Date")
                case "YYYYMMDD":
                    transfer_files(files, Source_path = self.source_path, Destination_path = self.destination_path, sort = "YYYYMMDD")
                case "YYYYDDMM":
                    transfer_files(files, Source_path = self.source_path, Destination_path = self.destination_path, sort = "YYYYDDMM")
                case "Sort by file type":
                    transfer_files(files, Source_path = self.source_path, Destination_path = self.destination_path, sort = "Type")
        # catch the error and create a pop up to warn user an error have occured
        except FileNotFoundError as e:
            popup = Popup_Frame(title = "Error occurred during file sorting",
                                text = "Error occured while accessing the source or destination, "
                                "this could be caused by file being\n removed during execution "
                                "restart the application and try again\n",
                                confirmation = False)
            popup.open()
    

class Popup_Frame(Popup):
    '''
    The popup class used to create warnings and confirm screens\n
    title: the title of the popup\n
    text: the content of the popup\n
    confirmation: confirm and cancel button if true, only a cancel button if false\n
    confirmed_callback: the function to be executed when the confirm button is pressed
    '''

    title = StringProperty('')
    text = StringProperty('')
    confirmation = BooleanProperty(None)
    confirmed_callback = ObjectProperty(None)
    # if the attribute confirmation is true then execute the attribute confirmed_callback
    def confirmation_action(self) -> None:
        if self.confirmed_callback:
            self.confirmed_callback()
        self.dismiss()


class Hand_Gesture_Frame(Screen):
    '''The Class that handels the logic of the Hand Gesture menu'''
    # access the json file and store the data then convert it into a python dictionary 
    with open('Storage.json', 'r') as f:
        # load the latest save of the setting
        file = json.load(f)
        point_left  = file['point_left']
        point_right = file['point_right']
        point_top    = file['point_up']
        point_bottom  = file['point_down']
        
    spinner_left  = StringProperty(point_left)
    spinner_right = StringProperty(point_right)
    spinner_up    = StringProperty(point_top)
    spinner_down  = StringProperty(point_bottom)

    toggle = BooleanProperty()
    display = BooleanProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = Counter()

    # called when the user choosed an option in spinner
    def update_pointer_option(self, id : int, text : str) -> None:
        # load the latest save of the json file and convert to python dictionary
        with open('Storage.json', 'r') as f:
            file = json.load(f)
            # update the corresponding option
            match id:
                case 0:
                    file["point_left"] = text
                    
                case 1:
                    file["point_right"] = text
                    
                case 2:
                    file["point_up"] = text
                    
                case 3:
                    file["point_down"] = text
                    
        # convert python dictionary to json object and save to .json file 
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)    


    # called when the hand gesture detects a hand pointing to a certain direction
    def hand_gesture_callback(self, direction) -> bool:
        """
        direction can be [TL, TN, TR, NL, NN, NR, BL, BN, BR]
        """
        # for displaying the states of the program
        # pause the main loop until the program is fully loaded
        if direction == "Ready":
            global loading_hand_gesture
            loading_hand_gesture = False

        direction = self.counter.check(direction)
        # load the setting
        with open('Storage.json', 'r') as f:
            file = json.load(f)
            point_left  = file['point_left']
            point_right = file['point_right']
            point_top    = file['point_up']
            point_bottom  = file['point_down']

        # check direction of the hand
        match direction:
            case "NL":
                match point_left:
                    case 'Last Song':
                        keyboard.send("previous track")
                    case 'Last Tab':
                        keyboard.send("alt+shift+esc")
                                
            case "TN":
                match point_top:
                    case 'Increase Volume':
                        keyboard.send("volume up")
                    case 'Apps Overview':
                        keyboard.send("win+tab")

            case "NR":
                match point_right:
                    case 'Next Song':
                        keyboard.send("next track")
                    case 'Next Tab':
                        keyboard.send("alt+esc")
                        
            case "BN":
                match point_bottom:
                    case 'Decrease Volume':
                        keyboard.send("volume down")
                    case 'Clear Screen':
                        keyboard.send("win+d")
            case _:
                pass 

        time.sleep(0.1)

        if self.toggle:
            # tell the hand gesture thread to exit
            return True
        else:
            return False
        

    # called when the user click start
    def start_stop_hand_gesture(self) -> None:
        debug_display = not self.display
        # if thread hand_gesture_function already running then exit this function
        for i in threading.enumerate():
            if "hand_gesture_function" in str(i):
                return

        global loading_hand_gesture
        loading_hand_gesture = True

        # start hand gesture detection
        thread = threading.Thread(target = hand_gesture_function, args = (self.hand_gesture_callback, debug_display), daemon=True)
        thread.start()
        # pause the main thread to allow the sub thread to load
        a = 0
        while loading_hand_gesture:
            time.sleep(0.5)
            # loading TUI
            match a:
                case 0:
                    print("loading    ",end='\r')
                case 1:
                    print("loading.    ",end='\r')
                case 2:
                    print("loading..    ",end='\r')
                case 3:
                    print("loading...    ",end='\r')
                    a = 0
            a += 1 


class Tab_Organizer_Frame(Screen):
    '''The Class that handels the logic of the Tab Organizer menu'''

    def switch_desktop(self, index : int) -> None:
        # execute switch_desktop
        if not switch_desktop(index):
            # if switch_desktop failed
            # open warning
            popup = Popup_Frame(
            title = "error",
            text = "failed to move to desktop " + str(index + 1),
            confirmation = False
            )
            popup.open()


class Setting_Shortcut_Frame(Screen):
    '''The Class that handels the logic of the Shortcut Setting menu'''

    # initialis the state of each parameter type
    buttons = ListProperty([[False,False,False,False],
                            [False,False,False,False],
                            [False,False,False,False],
                            [False,False,False,False]])
    shortcut_names = ['','','','']
    # load setting
    with open('Storage.json', 'r') as f:
        file = json.load(f)

        temp_button_1 = file['button_1']
        temp_button_2 = file['button_2']
        temp_button_3 = file['button_3']
        temp_button_4 = file['button_4']

        keybind = StringProperty(file["overlay_shortcut"])
        
        shortcut_names[0] = file['shortcut_names'][0]
        shortcut_names[1] = file['shortcut_names'][1]
        shortcut_names[2] = file['shortcut_names'][2]
        shortcut_names[3] = file['shortcut_names'][3]
    
    # a list containing the data of each button 
    button_assing = ListProperty([temp_button_1, temp_button_2, temp_button_3, temp_button_4])

    # apply setting
    spinner_current_1_1 = StringProperty(temp_button_1['type'])
    spinner_current_1_2 = StringProperty(temp_button_1['parm'])
    spinner_current_1_3 = StringProperty(temp_button_1['parm'])
    spinner_current_1_4 = StringProperty(temp_button_1['parm'])
    spinner_current_1_5 = StringProperty(temp_button_1['parm'])
    
    spinner_current_2_1 = StringProperty(temp_button_2['type'])
    spinner_current_2_2 = StringProperty(temp_button_2['parm'])
    spinner_current_2_3 = StringProperty(temp_button_2['parm'])
    spinner_current_2_4 = StringProperty(temp_button_2['parm'])
    spinner_current_2_5 = StringProperty(temp_button_2['parm'])

    spinner_current_3_1 = StringProperty(temp_button_3['type'])
    spinner_current_3_2 = StringProperty(temp_button_3['parm'])
    spinner_current_3_3 = StringProperty(temp_button_3['parm'])
    spinner_current_3_4 = StringProperty(temp_button_3['parm'])
    spinner_current_3_5 = StringProperty(temp_button_3['parm'])

    spinner_current_4_1 = StringProperty(temp_button_4['type'])
    spinner_current_4_2 = StringProperty(temp_button_4['parm'])
    spinner_current_4_3 = StringProperty(temp_button_4['parm'])
    spinner_current_4_4 = StringProperty(temp_button_4['parm'])
    spinner_current_4_5 = StringProperty(temp_button_4['parm'])

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # load the setting for the gui
        match self.temp_button_1['type']:

            case 'start_application':
                self.buttons[0] = [True,False,False,False]

            case 'switch_desktop':
                self.buttons[0] = [False,True,False,False]

            case 'move_window_to_desktop':
                self.buttons[0] = [False,False,True,False]

            case 'switch_to_app':
                self.buttons[0] = [False,False,False,True] 

        match self.temp_button_2['type']:

            case 'start_application':
                self.buttons[1] = [True,False,False,False]

            case 'switch_desktop':
                self.buttons[1] = [False,True,False,False]

            case 'move_window_to_desktop':
                self.buttons[1] = [False,False,True,False]

            case 'switch_to_app':
                self.buttons[1] = [False,False,False,True] 
        
        match self.temp_button_3['type']:

            case 'start_application':
                self.buttons[2] = [True,False,False,False]

            case 'switch_desktop':
                self.buttons[2] = [False,True,False,False]

            case 'move_window_to_desktop':
                self.buttons[2] = [False,False,True,False]

            case 'switch_to_app':
                self.buttons[2] = [False,False,False,True] 
        
        match self.temp_button_4['type']:

            case 'start_application':
                self.buttons[3] = [True,False,False,False]

            case 'switch_desktop':
                self.buttons[3] = [False,True,False,False]

            case 'move_window_to_desktop':
                self.buttons[3] = [False,False,True,False]

            case 'switch_to_app':
                self.buttons[3] = [False,False,False,True] 


    # called when confirm button is clicked
    def update_overlay_shortcut(self, text) -> bool:
        '''return False if failed'''
        # validate the shortcut keybind
        try:
            keyboard.is_pressed(text)
        except:
            popup = Popup_Frame(title = "shortcut keybind invalid",
                                text = "The keybind of overlay is invalid please change the keybind in the settings page",
                                confirmation = False)
            popup.open()
            return False
        
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        app.overlay_shortcut = text 

        with open('Storage.json', 'r') as f:
            file = json.load(f)
            file['overlay_shortcut'] = text
            
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)     

        return True

    # called when an option is chooesn
    def spiiner_type_select(self, id : int, text : str) -> None:
        
        # determind the function type  
        # update the parameter state of the GUI with the spinner id
        match text:
            
            case 'start_application':
                self.buttons[id] = [True,False,False,False]

            case 'switch_desktop':
                self.buttons[id] = [False,True,False,False]

            case 'move_window_to_desktop':
                self.buttons[id] = [False,False,True,False]

            case 'switch_to_app':
                self.buttons[id] = [False,False,False,True]
        
        # clear the parameter 
        self.button_assing[id] = {"type" : text, "parm" : ""}

        # clear the parameter of the spinner selected with the spinner id
        match id:
            case 0:
                self.spinner_current_1_2 = ''
                self.spinner_current_1_3 = ''
                self.spinner_current_1_4 = ''
                self.spinner_current_1_5 = ''
            
            case 1:
                self.spinner_current_2_2 = ''
                self.spinner_current_2_3 = ''
                self.spinner_current_2_4 = ''
                self.spinner_current_2_5 = ''
        
            case 2:
                self.spinner_current_3_2 = ''
                self.spinner_current_3_3 = ''
                self.spinner_current_3_4 = ''
                self.spinner_current_3_5 = ''

            case 3:
                self.spinner_current_4_2 = ''
                self.spinner_current_4_3 = ''
                self.spinner_current_4_4 = ''
                self.spinner_current_4_5 = ''
        
    # called by the GUI
    def update_parameter(self, id, parameter, type) -> None:
        '''update the parameter of the button'''
        self.button_assing[id] = {"type" : type, "parm" : parameter}

        
    # when the confirm button is clicked
    def confirm(self) -> None:
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        # check if any parameter in option is empty
        for i in self.button_assing:
            if i == {} or i['parm'] == '':
                # display warning
                popup = Popup_Frame(
                    title = "empty attribute",
                    text = "some options are empty, please fill in all options and retry",
                    confirmation = False
                )
                popup.open()
                return None
            
        # validate and update shortcut
        if not self.update_overlay_shortcut(self.keybind):
            # stop upodating the value
            return None
        
        # load and update data from storage
        with open('Storage.json', 'r') as f:
            file = json.load(f)

            temp_button_1 = file['button_1']
            temp_button_2 = file['button_2']
            temp_button_3 = file['button_3']
            temp_button_4 = file['button_4']

            temp_button_1['type'] = self.button_assing[0]['type']
            temp_button_1['parm'] = self.button_assing[0]['parm']
            temp_button_2['type'] = self.button_assing[1]['type']
            temp_button_2['parm'] = self.button_assing[1]['parm']
            temp_button_3['type'] = self.button_assing[2]['type']
            temp_button_3['parm'] = self.button_assing[2]['parm']
            temp_button_4['type'] = self.button_assing[3]['type']
            temp_button_4['parm'] = self.button_assing[3]['parm']

            file['button_1'] = temp_button_1
            file['button_2'] = temp_button_2
            file['button_3'] = temp_button_3
            file['button_4'] = temp_button_4

            file['shortcut_names'][0] = self.shortcut_names[0]
            file['shortcut_names'][1] = self.shortcut_names[1]
            file['shortcut_names'][2] = self.shortcut_names[2]
            file['shortcut_names'][3] = self.shortcut_names[3]
            app.shortcut_names[0] = self.shortcut_names[0]
            app.shortcut_names[1] = self.shortcut_names[1]
            app.shortcut_names[2] = self.shortcut_names[2]
            app.shortcut_names[3] = self.shortcut_names[3]

        # save the changes to the storage
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)

    
    def update_name(self, id, text) -> None:
        '''update button name'''
        self.shortcut_names[id] = text  


class Setting_Color_Frame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    # load the parameter from files 
    with open('Storage.json', 'r') as f:
        user_data = json.load(f)

        temp_1 = user_data.get('text_color', [0,0,0,1])
        temp_2 = user_data.get('background_color', [1,1,1,1])
        temp_3 = user_data.get('button_color', [1,1,1,1])
        
        # color_1 : text color
        # color_2 : background color
        # color_3 : button color
        color_1 = ListProperty(temp_1)
        color_2 = ListProperty(temp_2)
        color_3 = ListProperty(temp_3)
    

    def set_text_theme(self, n, value) -> None:
        '''update the "value" to the storage and vairables'''
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        self.color_1[n] = value
        # update the color in GUI
        app.text_color = self.color_1  

        # load the data from storage
        with open('Storage.json', 'r') as f:
            file = json.load(f)
            # update the value to the data
            file['text_color'] = self.color_1
        
        # update data to storage
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)

        
    def set_background_theme(self, n, value) -> None:
        '''update the "value" to the storage and vairables'''
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        self.color_2[n] = value
        # update the color in GUI
        app.background_color = self.color_2  
        
        # load the data from storage
        with open('Storage.json', 'r') as f:
            file = json.load(f)
            file['background_color'] = self.color_2

        # update data to storage
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)
            

    def set_button_theme(self, n, value) -> None:
        '''update the "value" to the storage and vairables'''
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        self.color_3[n] = value
        # update the color in GUI
        app.button_color = self.color_3  
        
        # load the data from storage
        with open('Storage.json', 'r') as f:
            file = json.load(f)
            file['button_color'] = self.color_3

        # update data to storage
        with open('Storage.json', 'w') as f:
            json.dump(file, f, indent = 4)
            

class Overlay_Frame(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_key_pressed = False
        self.is_overlay_opened = False
        # this number is to calabrate to the scale in the windows setting
        self.screen_size_calabration = 1.00

        # create thread for listenling keybind passively 
        Clock.schedule_interval(self.overlay_ui, 0.1)

        
    def overlay_ui(self, _dt) -> None:
        '''listen to keyboard and open gui'''
        # get the Kivy App api to access the vairable used in ui
        app = App.get_running_app()
        
        # if the shortcut keybind is pressed
        # when the key is holding
        if keyboard.is_pressed(app.overlay_shortcut): 
             
            # when the key pressed is registered for the first time
            if not self.overlay_key_pressed:
                # update the key press register 
                self.overlay_key_pressed = True
                
                # first click
                # if the overlay is not opened yet
                if not self.is_overlay_opened:
                    # store the current focused window
                    self.current_window = get_current_window()
                    # store the opened screen of the program
                    self.original_screen = self.manager.current
                    # store the size of the screen window of the program
                    self.original_size = Window.system_size
                    # disable transition temporarily
                    self.manager.transition = kivy.uix.screenmanager.NoTransition()  
                    # change the screen to overlay screen
                    self.manager.current = 'Overlay'
                    # set the size to 400 pixel width and 400 pixel height
                    Window.system_size = (400,400)
                    # bring the program to the top of the window
                    Window.restore()
                    # store the position of the program
                    self.original_pos = Window.left, Window.top
                    # set the position of the center of the window to the mouse location 
                    Window.left = mouse_position()[0] / self.screen_size_calabration - 200
                    Window.top  = mouse_position()[1] / self.screen_size_calabration - 200

                    # restore transition
                    self.manager.transition = kivy.uix.screenmanager.SlideTransition()  
                    
                    # update the overlay state register
                    self.is_overlay_opened = True

                # second click
                # if the overlay is already opened
                else:
                    # close the overlay
                    self.close_overlay()
                    # update the overlay state register
                    self.is_overlay_opened = False
        
        # key released 
        # when the key is not holding anymore
        elif self.overlay_key_pressed:
            # update the key press register
            self.overlay_key_pressed = False


    def close_overlay(self, minimize : bool = True, resize : bool = True, RTH : bool = True) -> None:
        '''
        restore the program GUI to where it was before the overlay is opened\n
        minimize : minimize the windows
        resize : restore program GUI to the original size before the overlay
        RTH : (return to home) return to the original screen in the program
        '''
        # bring the program to the focus
        Window.restore()
        
        if resize:
            # restore program GUI to the original size before the overlay
            Window.system_size = self.original_size
        if RTH:
            # disble transition temporarily
            self.manager.transition = kivy.uix.screenmanager.NoTransition()  
            # restore the size 
            self.manager.current = self.original_screen 
            # restore transition
            self.manager.transition = kivy.uix.screenmanager.SlideTransition()  

        # restore the position of the program
        Window.left = self.original_pos[0] 
        Window.top  = self.original_pos[1] 

        # minimize the program
        def delay(dt):
            Window.minimize()
            
        if minimize:
            # wait for 0.4 second before minimize
            Clock.schedule_once(delay, 0.4)
    

    def function(self, func_type : str, parameter : str) -> None:
        '''function called by button in kv file'''

        # check which function is selected
        match func_type:

            # if switch_to_app is selected
            case "switch_to_app":
                self.manager.current = parameter
                # close overlay and restore window
                self.close_overlay(minimize = False, RTH = False)
            
            # if switch_desktop is selected
            case "switch_desktop":
                # calculate the correct index for function switch_desktop
                index = int(parameter[-1]) - 1
                # if switch_desktop run successfully
                if switch_desktop(index):
                    # close overlay, restore window and minimize window
                    self.close_overlay()
                else:
                    # if error occured during switch_desktop
                    # create a popup
                    popup = Popup_Frame(
                        title = "error",
                        text = "failed to move to desktop " + parameter,
                        confirmation = False
                    )
                    # display popup
                    popup.open()
                    # close overlay and restore window 
                    self.close_overlay(minimize = False)

            # if move_window_to_desktop is selected
            case "move_window_to_desktop":
                # calculate the correct index for function switch_desktop
                index = int(parameter[-1]) - 1
                # if move_window_to_desktop run successfully
                if move_window_to_desktop(index, self.current_window):
                    # close overlay, restore window and minimize window
                    self.close_overlay()
                else:
                    # if error occured during move_window_to_desktop
                    # create a popup
                    popup = Popup_Frame(
                        title = "error",
                        text = "failed to move window to desktop " + parameter,
                        confirmation = False
                    )
                    # display popup
                    popup.open()
                    # close overlay and restore window 
                    self.close_overlay(minimize = False)
            
            # if start_application is selected
            case "start_application":
                # if start_application run successfully
                if start_application(parameter):
                    # close overlay, restore window and minimize window
                    self.close_overlay()
                else:
                    # if error occured during start_application
                    # create a popup
                    popup = Popup_Frame(
                            title = "error",
                            text = "failed to open " + parameter,
                            confirmation = False
                        )
                    # display popup
                    popup.open()
                    # close overlay and restore window 
                    self.close_overlay(minimize = False)


    def button_function(self, id) -> None:
        '''called when button is clicked, the wrapper before function execute'''
        
        # load data from storage
        with open('Storage.json', 'r') as f:
            file = json.load(f)
        
        # check which button is clicked
        match id:
            # if button 1 is selected
            case 1:
                # load the setting for button 1
                button = file.get('button_1')
                # load the function type of button 1
                func_type = button["type"]
                # load the function parameter of button 1
                parameter = button["parm"]
                # execute function
                self.function(func_type, parameter)
                
            # if button 2 is selected
            case 2:
                # load the setting for button 2
                button = file.get('button_2')
                # load the function type of button 2
                func_type = button["type"]
                # load the function parameter of button 2
                parameter = button["parm"]
                # execute function
                self.function(func_type, parameter)
                            
            # if button 3 is selected
            case 3:
                # load the setting for button 3
                button = file.get('button_3')
                # load the function type of button 3
                func_type = button["type"]
                # load the function parameter of button 3
                parameter = button["parm"]
                # execute function
                self.function(func_type, parameter)

            # if button 4 is selected
            case 4:
                # load the setting for button 4
                button = file.get('button_4')
                # load the function type of button 4
                func_type = button["type"]
                # load the function parameter of button 4
                parameter = button["parm"]
                # execute function
                self.function(func_type, parameter)

        # update the overlay state
        self.is_overlay_opened = False
        
        
# The development of the structure of window_manager is referenced to this post from stackoverflow
# https://stackoverflow.com/questions/34787525/kivy-changing-screen-from-python-code
class window_manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # add the "Frame"s to widget so the screen can be accessable by the kivy libary using ScreenManager
        self.add_widget(Welcome_Frame(name='Welcome'))
        self.add_widget(Main_Page_Frame(name='Main_Page'))
        self.add_widget(File_Sorter_Frame(name='File_Sorter'))
        self.add_widget(Hand_Gesture_Frame(name='Hand_Gesture'))
        self.add_widget(Tab_Organizer_Frame(name='Tab_Organizer'))
        self.add_widget(Setting_Color_Frame(name='Settings_Color'))
        self.add_widget(Setting_Shortcut_Frame(name='Settings_Shortcut'))
        self.add_widget(Overlay_Frame(name='Overlay'))
        # self.add_widget(The_name_of_class(name='any_name_you_want'))
        
        # jump to the main page after 2 seconds when allowing the program continue to run
        Clock.schedule_once(self.load_screen, 2)
        
        # display the welcome screen
        self.current = 'Welcome'

        # bring the app to the top and put focus on the app
        Window.restore()
        # wait for 0.1s for the app to go to the top
        time.sleep(0.1)
        # pin the program in windows so it will show up on all virtual desktops
        pin()


    def load_screen(self, _) -> None:
        '''display the menu'''
        self.current = 'Main_Page'


class KivyApp(App):
    '''The main application class'''
    
    # disable the "mutitouch" feature which create effect unwanted
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    
    # load all datas from Storage.json in to the program  
    with open('Storage.json', 'r') as json_file:
        # convert the json object in vairable "json_file" into python dictionary and store in vairable "file"
        file = json.load(json_file)
        
        # from the dictionary "file" store the items of the key "text_color" in vairable text_color
        # if the text_color is empty or not exist, store a defualt value of [0,0,0,1] in text_color instead
        # text_color is store as a list property of KivyApp
        # etc... 
        text_color = ListProperty(file.get('text_color', [0,0,0,1]))
        background_color = ListProperty(file.get('background_color', [1,1,1,1]))
        button_color = ListProperty(file.get('button_color', [1,1,1,1]))
        display_text = StringProperty(file.get('display_text', "Welcome"))
        overlay_shortcut = StringProperty(file.get('overlay_shortcut', 'ctrl+d'))
        shortcut_names = ListProperty(file['shortcut_names'])

    # store the current as a string property of KivyApp
    time = StringProperty(get_time())
    date = StringProperty(get_date())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # call update_value function every 1s
        Clock.schedule_interval(self.update_value, 1)

    def update_value(self, dt):
        '''update time'''
        # update current time
        self.time = get_time()
        # update current date
        self.date = get_date()

    def build(self):
        return window_manager()

# if the program is directly run and not imported
if __name__ == "__main__":
    # start program
    KivyApp().run()
