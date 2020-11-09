from bs4 import BeautifulSoup
import json,os,re

class Monster:
    def __init__(self, name,mon_type, size, alignment, armor_class, hit_points, speed, atributes,challenge,traits_and_actions):
        self.name = name
        self.mon_type = mon_type
        self.size = size
        self.alignment = alignment
        self.armor_class = armor_class
        self.hit_points = hit_points
        self.speed = speed
        self.atributes = atributes
        self.challenge = challenge
        self.traits_and_actions = traits_and_actions

    def __str__(self):
        return("""
Name: %s\n
Type: %s\n
Size: %s \n
Alignment: %s \n
AC: %s \n
HP: %s \n
Speed: %s \n
Atributes: %s \n
Challenge: %s \n
Traits and Actions:
        %s \n 
            """%(self.name, self.mon_type, self.size, self.alignment, self.armor_class, self.hit_points, self.speed,self.atributes,self.challenge,self.traits_and_actions))


def create_monster(insoup):
    line_list = insoup.get_text().strip().split("\n")
    line_list = [name for name in line_list if name.strip()]
    
    if "name=" in line_list[0]:
        line_list = line_list[1:]
    #print(line_list)
    mon_list = list()
    for el in line_list:
        #print(el.strip())
        mon_list.append(el.strip())
    print(mon_list)

    name = mon_list[0].lower()
    mon_type = mon_list[1].split()[1].replace(",","").lower()
    size = mon_list[1].split()[0].lower()
    print(mon_list[1])
    alignment = mon_list[1].split(",")[1].lower()
    armor_class = int(mon_list[3].split()[0])
    hp = int(mon_list[5].split()[0])
    speed_list = [0,0,0,0,0] #speed,burrow,climb,fly,swim
    speeds = mon_list[7].split(",")
    print(speeds)
    for nums in speeds:
        if "burrow" in nums:
            speed_list[1] = int(nums.split()[1])
        elif "climb" in nums:
            speed_list[2] = int(nums.split()[1])
        elif "fly" in nums:
            speed_list[3] = int(nums.split()[1])
        elif "swim" in nums:
            speed_list[4] = int(nums.split()[1])
        else:
            speed_list[0] = int(nums.split()[0])
    print(speed_list)
    attribute_list = list()
    for i in range(14,20):
        attribute_list.append(int(mon_list[i].split("(")[0]))
    for i in range(20,1000):
        if mon_list[i] == "Challenge":
            challenge = mon_list[i+1].split()[0]
            mon_list.pop(i)
            mon_list.pop(i)        
            break
    traits = "\n".join(mon_list[20:]).strip()
    m = Monster(name,mon_type,size,
        alignment,armor_class,hp,speed_list,attribute_list,challenge,traits)
    print(m.name)
    return m

def save_mon(monster):
    mon_dict = dict()
    mon_dict["name"] = monster.name
    mon_dict["type"] = monster.mon_type
    mon_dict["size"] = monster.size
    mon_dict["alignment"] = monster.alignment
    mon_dict["armor_class"] = monster.armor_class
    mon_dict["hp"] = monster.hit_points
    mon_dict["speed"] =monster.speed
    mon_dict["attributes"] = monster.atributes
    mon_dict["challenge"] = monster.challenge
    mon_dict["traits_and_actions"] = monster.traits_and_actions
    


    if not os.path.exists('monsters_json/%s' % monster.mon_type):
        os.makedirs('monsters_json/%s' % monster.mon_type)
    with open("monsters_json/%s/%s.json"%(monster.mon_type,monster.name),"w+") as f:
        json.dump(mon_dict,f,indent=4)
   

def create_soup(infile):
    soup_list = list()
    with open(infile) as f:
        soup = BeautifulSoup(f, 'lxml')
    body_list = soup.find_all("a", {"id" : re.compile('a.*')})
    print(len(body_list))
    #print(body_list)
    if len(body_list) < 1: 
        soup_list.append(soup)
    else:
        print("multiple monsters in this file!")
        split_file = soup.prettify().split("<a id=")
        split_file = split_file[1:]
        for mons in split_file:
            mon_soup = BeautifulSoup(mons, 'lxml')
          
            soup_list.append(mon_soup)
    #print(soup_list)
    return soup_list
            


root = os.curdir + "/monsters"
for path, subdirs, files in os.walk(root):
    for name in files:
        file_path = os.path.join(path, name)
        print(file_path)
        mon_list2 = create_soup(file_path)
        for mons in mon_list2:
            if len(mon_list2) > 0:
                m = create_monster(mons)
                save_mon(m)
