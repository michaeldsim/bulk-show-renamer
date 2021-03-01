import os
import argparse
import shutil

parser = argparse.ArgumentParser(description="A program created to make it easier to rename files in bulk. Primarily made for renaming media.")
parser.add_argument("-s", "--separate_dirs", help="Enabling this will separate the seasons into separate folders.", action='store_true')
parser.add_argument("--input_path", help="Set a custom input folder. Otherwise, it will use \"./input/\" as the default", default="./input/")
args = parser.parse_args()
sep_dirs = args.separate_dirs
input_path = args.input_path

files = []

def rename(prepare):
    i = 1
    j = 1

    for filename in files:
        extension = os.path.splitext(filename["old_name"])[1]
        filename["new_name"] = show + '.S'+ "{:02d}".format(j) +'E'+ "{:03d}".format(i) + extension

        if not prepare:
            os.rename(os.path.join(input_path, filename["old_name"]), os.path.join(input_path, filename["new_name"]))
        
            if sep_dirs:
                dir_name = input_path + "Season " + str(j) + "/"

                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
                
                if os.path.exists(dir_name):
                    file_path = input_path + filename["new_name"]
                    shutil.move(file_path, dir_name)

            print("Renaming " + "{:15s}".format(filename["old_name"]) + " => " + filename["new_name"])

        if(j == seasons and i == season[j]):
            if not prepare:
                print("==================")
                print("Process completed.")
            break

        if(season[j] != i):
            i += 1
        else:
            j += 1
            i = 1

def get_files():
    i = 1

    for filename in os.listdir(input_path):
        if i < total_episodes:
            files.append(
                {
                    "old_name" : filename,
                    "new_name" : "temp"
                }
            )

        i += 1
    
    if i > total_episodes:
        raise Exception("Episodes accounted for was {}. Total files counted in directory was {}".format(total_episodes, i))

def generate_table():
    rename(True)

    print("+" + 30*"-" +"+----+" + 30*"-" + "+")
    print("|" + "{:^30s}".format("Old Name") + "| => |" +"{:^30s}".format("New Name") +"|")
    print("+" + 30*"-" +"+----+" + 30*"-" + "+")
    for filename in files:
        print("|" + "{:^30s}".format(filename["old_name"][:30]) + "| => |" +"{:^30s}".format(filename["new_name"]) +"|")
    print("+" + 30*"-" +"+----+" + 30*"-" + "+")

show = input("Enter name of the show:\n")
seasons = int(input("Enter amount of seasons:\n"))

season = {}
total_episodes = 0

for i in range(seasons):
    episodes = int(input("Enter amount of episodes in season " + str(i+1) + ":\n"))
    season[i+1] = episodes
    total_episodes += episodes

get_files()
generate_table()

confirm = input("Does this look okay? Enter y/yes to continue.\n")

if confirm == 'y' or confirm == 'yes':
    rename(False)