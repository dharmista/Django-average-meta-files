import urllib
import urllib2

#Regular semester URL's
urls=[
    "http://www.gvpce.ac.in/results/B.TechIsemester(R-2013)RegularAutonomousExaminationsResultheldonFebruary-2014/find_info.asp",
    "http://www.gvpce.ac.in/results/BTechIISemReg-June2014/find_info.asp",
    "http://www.gvpce.ac.in/results/BTechIIISemReg(R2013)-Dec2014/find_info.asp",
    "http://www.gvpce.ac.in/results/B.Tech%20IVSemReg(R-2013)_May2015/find_info.asp",
    "http://www.gvpce.ac.in/results/B.TECHV(Reg)(R-2013)_November2015/find_info.asp",
    "http://www.gvpce.ac.in/results/B.Tech%20VI%20Sem%20Reg(R-2013)_April2016/find_info.asp",
    None,
    None
]

#Supplementary  results
urls_sup=[
    "http://www.gvpce.ac.in/results/BTechISemSupply%28R2013%29-June2014/find_info.asp",
    "http://www.gvpce.ac.in/results/BTechIISemSupply%28R2013%29-Dec2014/find_info.asp",
    "http://www.gvpce.ac.in/results/B.TechIIISemSupply(R2013)-May2015/find_info.asp",
    "http://www.gvpce.ac.in/results/B.Tech%20IV%20Sem%20(Sup)%20(R-2013)%20_%20May%202016/find_info.asp",
    "http://www.gvpce.ac.in/results/B.Tech%20V%20Sem%20(Sup)%20(R-2013)%20_%20April%202016/find_info.asp",
    None,
    None,
    None
]

#Revaluation results
urls_reval=[
    "http://www.gvpce.ac.in/results/BTechISemRegRev(R-2013)-Feb2014/find_info.asp",
    "http://www.gvpce.ac.in/results/BTechIISemReg(R-2013)RevJune2014/find_info.asp",
    "http://www.gvpce.ac.in/results/B.TechIIISemReg(R2013)RevDec2014/find_info.asp",
    "http://www.gvpce.ac.in/results/B.TechIVSemReg(R-2013)Rev_May2015/find_info.asp",
    "http://www.gvpce.ac.in/results/B.TechVSemReg&Sup(R-2013)Rev_Nov2015/find_info.asp",
    None,
    None,
    None

]

cut_offs=[]

class get_average:
    def __init__(self,sem,roll):
        self.sem = sem
        self.roll = roll
        self.escapes = ['Regd. No.','Name','Aggregate','Subject',None,'13NM1101','13NM1102','13NM1103']
    def average(self,method='reg'):
        if method=='reg':
            url = urls[self.sem-1]
        elif method=='reval':
            url = urls_reval[self.sem-1]
        else:
            url = urls_sup[self.sem-1]
        if url is None:
            return ""
        query_args = { 'u_input' : self.roll,'u_field' : 'state','B2':'Clear' }
        data = urllib.urlencode(query_args)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        html = response.read()
        #self.html = html
        return html

    def subject_marks(self,marks,cless,metas,marks_effected,marks_by_sups):
        sub_marks={}
        for row in marks:
            if row not in self.escapes:
                sub_marks[marks[row][0]] = marks[row][3]
        cless_subs = {}
        for row in cless:
            cless_subs[cless[row][0]] = cless[row][3]
        if cless_subs=={}:
            cless_subs=None
        return sub_marks,cless_subs,metas,marks_effected,marks_by_sups