# Author: Tyler Stoney, 2019
# install_deps.py
# Purpose: Scans a file for valid import statements,
#          parses all packages, and attempts to install them
#          if not found in your python installation.

import re, sys

def find_deps(lines):
    """
    @brief      given a list of lines in a file, compile a list of valid imports
    
    @param      lines  The file's lines
    
    @return     A list of dependencies for that file
    """

    deps = []

    # This regex ignores commented imports or things that may be misinterpreted
    # as an import in comments
    regex = re.compile(r"[^#]*(?<!#)([^#]*(?:from)?[^#]*(?:import)[^#])")
    for line in lines:
        print(line)
        if regex.match(line):
            overarching_line = line.split(';')
            for l in overarching_line:
                line = l.split()
                if line[0] == "import" or len(line) == 2:
                    for d in range(1, len(line), 1):
                        if line[d] == 'as' or line[d].startswith("#"):
                            break
                        # dep = line[1].split(",")[0].split(".")
                        dep = line[d].rstrip(',')
                        deps.append(dep)
                        pass
                else:
                    for i in range(len(line)):
                        token = line[i]
                        if token == "from":
                            dep = line[i+1].split(".")[0]
                            deps.append(dep)
                            break
                        elif token.startswith("#"):
                            break

    return deps

def install_deps(deps_set):
    """
    @brief      From a list of imports, install each if it can't be found
    
    @param      deps_set  The list of unique dependencies
    
    @return     Whether there were any to be installed
    """
    pre_installed = 0
    import os
    for dep in deps_set:
        try:
            new_module = __import__(dep)
            pre_installed += 1
        except ImportError as e:
            print("Don't have ", dep)
            cmd = "pip3 install -U " + dep
            os.system(cmd)
            pass # module doesn't exist, deal with it.

    return pre_installed == len(deps_set)


def main():
    deps = []

    file_list = sys.argv[1:]

    if len(file_list) == 0:
        print("Error: no file(s) given as argument(s)")
        sys.exit(1)

    for file in file_list:
        with open(file) as f:
            lines = f.read().split("\n")
            deps += find_deps(lines)

    deps_set = list({*[dep for dep in deps]})
    print(deps_set)

   # if install_deps(deps_set):
   #     print("Already got everything!")
   # else:
   #     print("You should be caught up now.")

if __name__ == '__main__':
    main()
