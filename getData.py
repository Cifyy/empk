from zipfile import ZipFile
import urllib.request,os,time

def getLastDateFromFile(path):
    if not os.path.exists(path): return "noPathFound"
    return time.strftime("%Y-%m-%d-%H:%M", time.strptime(time.ctime(os.path.getmtime(path))))

def updateVersionFile(busDate,tramDate):
    if not os.path.exists("version.txt"):
        open("version.txt", "x").close()
    f = open("version.txt","w")
    f.truncate(0)
    f.seek(0)
    f.writelines(busDate+"\n")
    f.writelines(tramDate)
    f.close()

def readVersionFile():
    if not os.path.exists("version.txt"): return 
    nwf = open("version.txt", "r")
    dates = nwf.readline()[:-1],nwf.readline()
    nwf.close()
    return dates

def fetchNewData():
    try:
        urllib.request.urlretrieve("https://gtfs.ztp.krakow.pl/GTFS_KRK_A.zip", r"RawData\B_Data.zip")
        urllib.request.urlretrieve("https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip", r"RawData\T_Data.zip")
    except:
        print("Cannot Fetch Data")

    if not os.path.exists(r"RawData\B_Data.zip") or not os.path.exists(r"RawData\T_Data.zip"):
        return False
    
    with ZipFile(r"RawData\B_Data.zip", 'r') as zip_ref:
        zip_ref.extractall(r"RawData\B_Data")
    with ZipFile(r"RawData\T_Data.zip", 'r') as zip_ref:
        zip_ref.extractall(r"RawData\T_Data")

    return True
        
def clear(line,itk):
    cur,lastComa,result = 0,0,[]
    for i, c in enumerate(line):
        if c != ',' and i != len(line)-1 : continue
        cur += 1
        if cur in itk :
            if c == ',' : result.append(line[lastComa:i])
            else : result.append(line[lastComa:i+1]) 
        lastComa = i+1
    return result

def getEntries(path1, itk):
    entries = []
    if not os.path.exists(path1): 
        print(path1,"is invalid")
        return 
    with open(path1, 'r', encoding = 'UTF-8') as file:
        for line in file: entries.append(clear(line.rstrip(),itk))
    return entries


# tests
if __name__ == '__main__':
    # fetchNewData()

    
    print(readVersionFile())
    # print(checkVersion("2023-10-30-20:51:49"))
    # updateVersionFile("dwa43424323","321")
    # print(getLastDateFromFile("RawData\T_Data\stop_times.txt"))
