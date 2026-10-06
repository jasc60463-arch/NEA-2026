# reference
# https://www.w3schools.com/python/ref_os_walk.asp
# https://www.w3schools.com/python/ref_os_mkdir.asp


existing_folders = {}

def get_items(source_path: str) -> list[str]:
    ''' 
    Return a list containing all the names of the files in the given path. \n
    If there is a folder in the path, the folder will be automatically unpacked. \n
    Folders will not be included in the list.
    ''' 
    import os
    
    items = []
    try:
        # get all files in source path
        files = os.walk(source_path)
    except Exception as e:
        print('Error accessing the source', e)
    # iterate all file name and add them in a list
    for root, dirs, file_names in files:
        for file in file_names:
            items.append(file)
    return items


def check_existing_folders(Destination_path: str) -> None:
    '''
    store the name and path of the existing folders from the destination path 
    and store in the existing_folder vairable(dictionary). \n
    existing_folders = {folder_name : folder_path}
    '''
    import os

    global existing_folders
    temp_folder = {}
    # get all files in destination path
    check_path = os.walk(Destination_path)
    # iterate all files
    for root, dirs, files in check_path:
        # root -> file path : C:\photos\folder\subfolder
        
        path = str(root)
        # if the path is the root
        if path == Destination_path:
            continue
        path = path.split('\\')
        full_name = path[-1]

        # truncate the first 10 character of the file 
        name = full_name[:10]
        # path : subfolder
        # root : subfolder or subfolder...

        temp_folder.update({name : full_name})
    existing_folders = temp_folder    


def create_dir(name,
                Destination_path,
                notice_when_folder_already_existed = True, 
                notice_when_folder_created = True
                ) -> None:
    '''
    Create a new folder with the specified name in the destination path.
    '''
    import os
    
    try:
        # create a new directory (folder)
        os.mkdir(f'{Destination_path}\\{name}')
    
    except FileExistsError:
        # directory already exist
        if notice_when_folder_already_existed: 
            # red text
            print(f'\033[91m  Folder {name} already exists  \033[00m')
    else:
        # directory successfully created
        if notice_when_folder_created:
            # green text
            print(f'\033[92m  Folder {name} created  \033[00m')


def transfer_files(files: list[str],
                    Source_path: str,
                    Destination_path: str,
                    sort: str = "C_Date", 
                    notice_when_file_already_existed = True,
                    notice_when_file_copied = True
                    ) -> None:
    '''
    C_Date : sort by creation date in the folder, it can be affected when the file is copied \n
    M_Date : sort by modification date doesn't affect when the file is copied, but it can be affected when the file is modified
    YYYYMMDD : extract first 8 number of the file name as date
    YYYYDDMM : extract first 8 number of the file name as date
    Type : sort by file type
    note: when the program executing and the source file have changed or been removed, the program may raise a FileNotFoundError
    '''
    import os
    from datetime import datetime
    import shutil

    for file in files:

        match sort:

            case "C_Date":
                # get the creation time of the file from windows
                time = os.path.getctime(f'{Source_path}\\{file}')
                # convert time into year_month_date
                date = datetime.fromtimestamp(time).strftime('%Y_%m_%d')

            case "M_Date":
                # get the modify time of the file from windows
                time = os.path.getmtime(f'{Source_path}\\{file}')
                # convert time into year_month_date
                date = datetime.fromtimestamp(time).strftime('%Y_%m_%d')

            case "YYYYMMDD":
                # filter non digit characters
                date = "".join(filter(str.isdigit, file))
                # convert time into year_month_date
                date = date[:4] + "_" + date[4:6] + "_" + date[6:8]

            case "YYYYDDMM":
                # filter non digit characters
                date = "".join(filter(str.isdigit, file))
                # convert time into year_month_date
                date = date[:4] + "_" + date[6:8] + "_" + date[4:6]

            case "Type":
                # seperate file type and file name
                file_name, file_type = os.path.splitext(file)
                # if file type (folder) is already exist in the destination
                if file_type in existing_folders.keys():
                    # the new path is assign to the existing folder
                    folder_name = existing_folders[file_type]
                else:
                    # create a new folder
                    create_dir(file_type, Destination_path)
                    # update the new folder to "existing_folder"
                    existing_folders[file_type] = file_type
                    # use file type as the new file name
                    folder_name = file_type
                # if file already existed in the folder
                if os.path.exists(f'{Destination_path}\\{folder_name}\\{file}'):
                    if notice_when_file_already_existed:
                        # yellow text
                        print(f'\033[93m  File {file} already exists in folder {folder_name}  \033[00m')       
                    # iterate next file
                    continue

                # copy the file
                shutil.copy2(f'{Source_path}\\{file}',f'{Destination_path}\\{folder_name}\\{file}')
                if notice_when_file_copied:
                    # Green text
                    print(f'\033[92m  File {file} copied to folder {folder_name}  \033[00m')
                # finish
                continue

        # date: yyyy_mm_dd
        # if file date (folder) is already exist in the destination
        if date in existing_folders.keys():
            # the new path is assign to the existing folder
            folder_name = existing_folders[date]
        else:
            # create a new folder
            create_dir(date, Destination_path)
            # use file date as the new file name
            folder_name = date
            # update the new folder to "existing_folder"
            existing_folders[date] = date

        # if file already existed in the folder
        if os.path.exists(f'{Destination_path}\\{folder_name}\\{file}'):
            if notice_when_file_already_existed:
                # yellow text
                print(f'\033[93m  File {file} already exists in folder {folder_name}  \033[00m')
        else:
            # copy the file
            shutil.copy2(f'{Source_path}\\{file}',f'{Destination_path}\\{folder_name}\\{file}')
            if notice_when_file_copied:
                # Green text
                print(f'\033[92m  File {file} copied to folder {folder_name}  \033[00m')

    
    
    

if __name__ == '__main__':
    exit()
    # Source_path = ''
    # Destination_path = ''

    # try:
    #     check_existing_folders(Destination_path)
    #     files = get_items(Source_path)
    #     transfer_files(files, Source_path = Source_path, Destination_path = Destination_path, sort = "Type")
    #     transfer_files(files, Source_path = Source_path, Destination_path = Destination_path, sort = "YYYYMMDD")
    # except FileNotFoundError as e:
    #     print('Error accessing the source or destination, this could be caused by file being removed during execution\n'
    #     'restart the application and try again\n', e)
    # transfer_files(files, sort = "C_Date")
    # transfer_files(files, sort = "YYYYMMDD")
