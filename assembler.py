#Tristan Mikiewicz and Josh Bekkerman
#I pledge my honor that I have abided by the Stevens Honor System
#Apex (Legends) Processing Unit
#12/9/2023

import os
def shift(string, num):
    while(len(string)<num):
        string = "0" + string
    return string

labels={}
currAddress=0x00

def instruc(ins):
    
    mc = 0b00000000000000000000000000000000

    
    symbol = ins[1]

    
    if symbol == "add":
        mc += 0b0 << 9  
        mc += 0b1 << 31  
    elif symbol == "sub":
        mc += 0b1 << 9  
        mc += 0b1 << 31  
    elif symbol == "load":
        mc += 0b1 << 2  
        mc += 0b1 << 31  
    elif symbol == "store":
        mc += 0b1 << 1  

   
    dest = ins[0]
    if symbol == "store":
        
        mc += int(dest[1]) << 15
    else:
        mc += int(dest[1]) << 28

    
    arg1 = ins[2]
    if arg1[0] == 'r':
        if symbol != "zero":
            mc += int(arg1[1]) << 24
    else:
        mc += 0b1 << 27  
        mc += int(arg1) << 19

    
    if symbol in ["load", "store"]:
        return mc

    
    arg2 = ins[3]
    if arg2[0] == 'r':
        mc += int(arg2[1]) << 15
    else:
        mc += 0b1 << 18  
        mc += int(arg2) << 10

    return mc


if __name__ == "__main__":
    if os.path.exists("ins"): 
        os.remove("ins")
    if os.path.exists("data"): 
        os.remove("data")

    file_name = open("assembly.txt", 'r')
    instr = open("ins", 'w')
    instr.write("v3.0 hex words addressed\n")

    dataW = False
    adl = 0x00
    instr.write(shift(hex(adl)[2:] + "0", 2) + " ")

    data_adl = 0x00
    count = 0
    dc = 0

    p_check = open("assembly.txt", 'r')
    for line in p_check:
        if not line.strip() or line.startswith(".text") or line.startswith("//"):
            continue
        if "//" in line:
            line = line[:line.find("//")]
        ins = line.split()
        if len(ins) > 1 and ins[1] == "label":
            mc = 0b0
            # Assuming labels is a dictionary defined elsewhere
            labels[ins[0]] = currAddress
        currAddress += 0x1

    for line in file_name:
        line = " ".join(line.split())
        if not line.strip() or line.startswith(".text") or line.startswith("//"):
            continue
        elif line.startswith(".data"):
            data = open("data", 'w')
            data.write("v3.0 hex words addressed\n")
            data.write(shift(hex(data_adl)[2:] + "0", 2) + " ")
            dataW = True
            continue

        if "//" in line:
            line = line[:line.find("//")]

        if dataW:
            data.write(shift(hex(int(line))[2:], 2) + " ")
            dc += 1
            if dc == 16:
                dc = 0
                data.write('\n')
                data_adl += 0x10
                if data_adl > 0xf0:
                    break
                data.write(hex(data_adl)[:2] + " ")
            continue

        ins = line.split()
        if ins[1] == "label":
            mc = 0b0
        else:
            mc = instruc(ins)

        instr.write(shift(hex(mc)[2:], 8) + " ")
        count += 1
        if count == 8:
            count = 0
            instr.write("\n")
            adl += 0x08
            if adl > 0xf8:
                break
            instr.write(shift(hex(adl)[2:], 2) + " ")

    while True:
        instr.write("00000000 ")
        count += 1
        if count == 8:
            count = 0
            instr.write("\n")
            adl += 0x08
            if adl > 0xf8:
                break
            instr.write(shift(hex(adl)[2:], 2) + " ")

    while True and dataW:
        data.write("00 ")
        dc += 1
        if dc == 16:
            dc = 0
            data.write("\n")
            data_adl += 0x10
            if data_adl > 0xf0:
                break
            data.write(hex(data_adl)[2:] + ": ")

    file_name.close()
    p_check.close()
    instr.close()
    if dataW:
        data.close()