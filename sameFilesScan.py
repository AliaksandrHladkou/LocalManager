import os
import collections
import json
import time
import filecmp

DEFAULT_PATH = r'C:\myFolder'

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
    except ValueError:
        print("Failed to write json data into %s" % file_name)

def filter_dict(dict, minimum=2):
    """ Reads data in dictionary and filters/sorts itmes based on name and
    minimum number of paths.

    Args:
        dict: Dictionary of files and its directories.
        minimum: Minimum number of required direcoties. OPTIONAL. Default is 2.

    Returns:
        filtered and sorted dictionary under single file name. 
    """
    filtered = {}
    for key, value in dict.items():
        if (len(value.items()) >= minimum):
            filtered[key] = {}
            for k1, v1 in value.items():
                filtered[key][k1] = v1
    return filtered

def get_files(starting_point=DEFAULT_PATH):
    """ Walks top-down thru all directories from starting point.

    Args:
        Starting Path; OPTIONAL

    Returns:
        List of tuples (path, dirs, files) scanned in directory.
    """
    listOfDir = []
    for (path, dirs, files) in os.walk(starting_point):
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
                if (filecmp.cmp(os.path.join(item1[0], key), os.path.join(item2[0], key))):
                    compared[key] = [item1[0], item2[0]]
    return compared


def main():
    starting = r'C:\exampleFolder'
    print("Reading from " + starting)
    
    start = time.time()

    files = get_files(starting)
    result = find_same_names(files, starting)
    filtered = filter_dict(result, 2)
    compared = compare_files(filtered)
    # write_json(filtered, 'filtered.json')
    write_json(compared, "sameFiles.json")

    end = time.time()
    print("It took: " + str(end- start))

if __name__ == '__main__':
    main()