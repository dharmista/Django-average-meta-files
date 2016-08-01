import index as baba
from bs4 import BeautifulSoup

offens = baba.get_average('','').escapes
urls   = baba.urls
revals = baba.urls_reval
sups   = baba.urls_sup

romans = ['I','II','III','IV','V','VI','VII','VIII']

def get_marks_dict(tables):
    if tables is None:
        return {},{},{}
    marks={}
    metas={}
    total = 0
    count=0
    credit_less={}
    for row in tables:
        sub = []
        for cell in row.children:
            sub.append(cell.string)
        if(len(sub) is 5):
            if sub[4]=='P' or sub[4]=='F':
                comp_sub = sub[0]
                pos = comp_sub.find('13')
                comp_sub.replace('-',' ')
                sub_code = comp_sub[pos:pos+9]
                comp_sub.replace(sub_code,'')
                splitted_sub = [sub_code,comp_sub]
                if (splitted_sub[0].find('13')):
                    splitted_sub[0], splitted_sub[1] = splitted_sub[1], splitted_sub[0]
                scode = str(splitted_sub[0].replace(' ', ''))
                if scode not in offens:
                    total += int(sub[3]);count+=1
                    splitted_sub[1] = str(splitted_sub[1]).lstrip()
                    k = [splitted_sub[1], ]+sub[1:]
                    marks[scode] = k
                else:
                    k = [splitted_sub[1], ]+sub[1:]
                    marks[scode] = k
                    credit_less[scode] = k
        elif len(sub)==2:
            metas[sub[0]] = sub[1]
    metas['total'] = total
    metas['count']=count
    return marks,metas,credit_less

def change_by_reval(marks,total,number,sem):
    mware = baba.get_average(sem,number)
    html_data = mware.average(method='reval')
    soup = BeautifulSoup(html_data, "html.parser")
    tables = soup.table
    marks_effected, metas, credit_less = get_marks_dict(tables)
    for x in marks_effected:
        total = total - int(marks[x][3])
        marks[x] = marks_effected[x]
        total += int(marks[x][3])
    return marks,marks_effected,total

def change_by_sups(marks,total,number,sem):
    mware = baba.get_average(sem,number)
    html_data = mware.average(method='sup')
    soup = BeautifulSoup(html_data, "html.parser")
    tables = soup.table
    marks_effected, metas, credit_less = get_marks_dict(tables)
    for x in marks_effected:
        if x not in offens:
            try:
                total = total - int(marks[x][3])
                marks[x] = marks_effected[x]
                total += int(marks[x][3])
            except Exception as e:
                print e
                pass
    return marks,marks_effected,total

def get_average(sem,num):
    adap = baba.get_average(sem,num)
    adap = adap.average()
    soup = BeautifulSoup(adap,"html.parser")
    tables = soup.table
    row_count=0
    marks,metas,credit_less = get_marks_dict(tables)
    temp={}
    temp['name'] = metas['Name']
    temp['roll'] = num
    return temp

def get_marks(sem,number):
    adap = baba.get_average(sem, number)
    adap = adap.average()
    soup = BeautifulSoup(adap, "html.parser")
    tables = soup.table
    row_count = 0
    marks,metas,credit_less = get_marks_dict(tables)
    marks,marks_effected,metas['total'] = change_by_reval(marks,metas['total'], number, sem)
    marks, marks_effected_by_sups, metas['total'] = change_by_sups(marks, metas['total'], number, sem)
    return baba.get_average(sem,number).subject_marks(marks,credit_less,metas,marks_effected,marks_effected_by_sups)

def show_all_sems(number):
    sem_map = [];metas={};sum=0
    for sem in range(1,9):
        if urls[sem-1] is not None:
            sub_marks,cless,metas,marks_effected,marks_by_sups = get_marks(sem,number)
            diff = float(metas['total'])/int(metas['count'])
            sem_map.append([sem,romans[sem-1],metas['total'],diff,int(metas['count'])*100])
            sum+=diff
    return sem_map,metas['Name'],(sum/len(sem_map)),len(sem_map)