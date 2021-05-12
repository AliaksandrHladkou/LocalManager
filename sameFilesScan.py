import os
import sys
import json
import time
import filecmp

DEFAULT_PATH = 'C:\\'

def find_same_names(files, starting_point=DEFAULT_PATH):
    """ Finds and groups files in directory that have same names
    
    Args:
        files: List representing files and its directories
        starting_point: Path to start reading from. OPTIONAL

    Returns:
        json object representing list of files along with their directories.
    """
    seen = {}

    for full_info in files:
        for file_name in full_info[2]:
            if not file_name in seen:
                # fsize = os.path.getsize(full_info[0])
                fsize = os.stat(full_info[0]).st_size
                seen[file_name] = {1: [full_info[0], fsize]}
            else:
                largest = 1 + find_largest_key(seen[file_name])
                # fsize = os.path.getsize(full_info[0])
                fsize = os.stat(full_info[0]).st_size
                seen[file_name][largest] = [full_info[0], fsize]
                # print('Found same name: %s' % file_name)
    return seen

def find_largest_key(dict):
    """ Finds largest number of key. Key must be an integer

    Args;
        Dictionary representing an object.

    Returns:
        Largest key of dictionary.
    """
    largest = 0
    for key, value in dict.items():
        if (key > largest):
            largest = key
    return largest

def write_json(data, file_name='data.json'):
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("%s was generated." % file_name)
    except ValueError:
        print("Failed to write json data into %s" % file_name)

def filter_dict(dict, ignoring_files, minimum=2):
    """ Reads data in dictionary and filters/sorts itmes based on name and
    minimum number of paths.

    Args:
        dict: Dictionary of files and its directories.
        ignoring_files: files to ignore
        minimum: Minimum number of required direcoties. OPTIONAL. Default is 2.

    Returns:
        filtered and sorted dictionary under single file name. 
    """
    filtered = {}
    for key, value in dict.items():
        if (len(ignoring_files) > 0):
            if (key in ignoring_files):
                continue
        if (len(value.items()) >= minimum):
            filtered[key] = {}
            for k1, v1 in value.items():
                filtered[key][k1] = v1
    return filtered

def get_files(ignoring_dir, starting_point=DEFAULT_PATH):
    """ Walks top-down thru all directories from starting point.

    Args:
        ignoring_dir: folders to ignore
        starting_point: path to start read from;  OPTIONAL

    Returns:
        List of tuples (path, dirs, files) scanned in directory.
    """
    listOfDir = []
    for (path, dirs, files) in os.walk(starting_point):
        if (all(items in ignoring_dir for items in dirs)):
            continue
        listOfDir.append((path, dirs, files))
    return listOfDir

def print_files_path(result):
    """ Prints files' paths to the console.

    Args:
        result: List of files and directories.
    """
    for item in result:
        for file_name in item[2]:
            print(file_name + " :: " + item[0])

def print_dirs(result):
    """ Prints directories

    Args:
        result: List of files and directories.
    """
    for item in result:
        if item[1]:
            print(item[1])

def print_full_info(result):
    """ Prints folders and files along with its directories.

    Args:
        result: List of files and directories.
    """
    for item in result:
        if item[1]:
            print(item[1])
        for file_name in item[2]:
            print(file_name + " :: " + item[0])

def compare_files(data):
    """ Compares whether files sorted by names are same. If true, adds to new json object.

    Args:
        data: json object representing files that are filtered and sorted based on their name.

    Returns:
        json object of compared files.
    """
    compared = {}

    for key, value in data.items():
        for i in range(1, len(data[key])-1):
            for j in range(i+1, len(data[key])):
                item1 = data[key][i]
                item2 = data[key][j]
                # print(key + " " + str(i) + " :: " + str(j))
                if (filecmp.cmp(os.path.join(item1[0], key), os.path.join(item2[0], key))):
                    compared[key] = [item1[0], item2[0]]
    return compared


def main():
    ignoring_files = ['.signature.p7s', 'LICENSE.TXT', 'THIRD-PARTY-NOTICES.TXT', 'useSharedDesignerContext.txt', 'version.txt']
    ignoring_dirs = ['archive']
    starting_path = ''

    if (len(sys.argv) > 1):
        starting_path = sys.argv[1]
    else:
        starting_path = DEFAULT_PATH
    
    if (os.path.exists(starting_path)):
        print("Reading from " + starting_path)
    
        start = time.time()

        files = get_files(ignoring_dirs, starting_path)
        result = find_same_names(files, starting_path)
        result = filter_dict(result, ignoring_files, 2)
        compared = compare_files(result)
        # write_json(filtered, 'filtered.json')
        write_json(compared, "sameFiles.json")

        end = time.time()
        print("It took: " + str(end- start))
    else:
        print("Specified path %s does not exists." % starting_path)

if __name__ == '__main__':
    main()