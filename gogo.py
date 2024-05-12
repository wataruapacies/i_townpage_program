import req_townp
import csv,time

with open("input_2.csv", 'r', encoding='cp932') as f:
    reader = csv.reader(f)
    for line in reader:
        where_list = line
        break
    print(len(where_list))
    what_list = ["介護"]
for i in range(len(where_list)):
    if i < 40 :
        continue
    print(i+1,"/",len(where_list),"-",where_list[i])
    for j in range(len(what_list)):
        #if i == 11 and j ==0:
        #    continue
        try:
            req_townp.doing(what_list[j],where_list[i])
        except:
            fe = open("err.txt","a")
            fe.writelines([what_list[j],",",where_list[i],"\n"])
            fe.close()
        time.sleep(10)
    time.sleep(10)