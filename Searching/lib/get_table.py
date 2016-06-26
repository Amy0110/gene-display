
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import DataFrame,Series
from lxml import html
import requests
import re
#x = html.parse("http://www.ncbi.nlm.nih.gov/clinvar/?term=NM_007294.3(BRCA1):c.5503C>T (p.Arg1835Ter)")



#'http://www.ncbi.nlm.nih.gov/clinvar/?term=NM_007294.3(BRCA1):c.5503C>T (p.Arg1835Ter)'


# In[ ]:

def get_table(url):
    print url
    urllist = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'}
    page = requests.get(url,headers=headers)

    x = html.fromstring(page.text.encode('utf-8'))

    flag = x.xpath("//span[@class='rev_stat_text']/text()")
    table1_col1 = x.xpath("//div[@id='_clinical-assertions']//td[1]/text()")
    table2_col2 = x.xpath("//div[@id='_summary-evidence']//tbody//td[1]/a/text()")
    table1_col2 = x.xpath("//div[@id='_clinical-assertions']//td[2]/text()")
    tmp = []
    for j in table1_col2:
        if j!='(' and j!=')':
            tmp.append(j)
    table1_col2=tmp
    table1_col2
    table1_col2_a = x.xpath("//div[@id='_clinical-assertions']//td[2]/a/text()")
    table1_col3 = x.xpath("//div[@id='_clinical-assertions']//tbody//td[3]/text()")
    table1_col4 = x.xpath("//div[@id='_clinical-assertions']//tbody//td[4]/ul[@class='pheno']/li/span[@class='phen_name']/text()")
    table1_col5 = x.xpath("//div[@id='_clinical-assertions']//td[5]/text()")

    table1_col6 = x.xpath("//div[@id='_clinical-assertions']//td[6]//li/a/text()")
    table1_col6_a = x.xpath("//div[@id='_clinical-assertions']//tbody//td[6]//li/a/@href")
    tmp = []
    re_extract = re.compile('<ul class="bottom-citations-list">(.*?)</ul>')
    item_match = re.findall(re_extract, page.content)
    count=0
    num = 0
    if item_match:
        for item_info in item_match:
            #if item_info!="":
            if count<len(table1_col5):
                if item_info=="":
                    tmp.append(" ")
                    count+=1
                else:
                    count+=1
                    tmp.append(table1_col6[num]+"["+"http://www.ncbi.nlm.nih.gov"+table1_col6_a[num]+"]")
                    urllist.append("http://www.ncbi.nlm.nih.gov"+table1_col6_a[num])
                    num+=1
    table1_col6 = tmp
    table1_col7 = x.xpath("//div[@id='_clinical-assertions']//td[7]/a/text()")
    table1_col8 = x.xpath("//div[@id='_clinical-assertions']//td[8]/text()")
    
    table1 = [[] for _ in range(8)]
    table2 = [[] for _ in range(8)]
    count = 0;
    for i in range(len(table1_col5)):
        if count+1<len(table1_col1) and table1_col1[count+1].strip()[0]=='(':
            table1[0].append(table1_col1[count]+table1_col1[count+1])
            count+=2
            #print table1_col1
        else:
            #print table1_col1[count][0]
            table1[0].append(table1_col1[count])
            count+=1
        table1[1].append(table1_col2[i])
        table1[2].append(table1_col3[i])
        table1[3].append(table1_col4[i].replace('\n',' '))
        table1[4].append(table1_col5[i])
        table1[5].append(table1_col6[i])
        table1[6].append(table1_col7[i])
        table1[7].append(table1_col8[i])
    table1 = DataFrame(table1).T
    table1.to_csv("/home/yindanping/gene/SearchGene/Searching/lib/tmpdata/table1",sep="\t",header=None)
    
   

    table2_col1 = x.xpath("//div[@id='_summary-evidence']//td[1]//text()")
    table2_col2 = x.xpath("//div[@id='_summary-evidence']//td[2]//text()")
    table2_col3 = x.xpath("//div[@id='_summary-evidence']//td[3]//text()")
    table2_col4 = x.xpath("//div[@id='_summary-evidence']//td[4]//text()")
    table2_col5 = x.xpath("//div[@id='_summary-evidence']//td[5]//text()")
    table2_col6 = x.xpath("//div[@id='_summary-evidence']//td[6]//text()")

    table2_col7 = x.xpath("//div[@id='_summary-evidence']//td[7]//text()")
    table2_col7_a = x.xpath("//div[@id='_summary-evidence']//tbody//td[7]/ul[@class='bottom-citations-list']/li[1]/a/@href")
    save_a = []
    for i in table2_col7_a:
        if i[0]!="#":
            save_a.append(i)
    table2_col7_a = save_a
    re_extract = re.compile('<td></td>')
    item_match = re.findall(re_extract, page.content)
    if item_match:
        tmp = [" ",]
    else:
        tmp=[]
    a_num=0
    i = 0
    while i<len(table2_col7):
        if table2_col7[i]=="Other citation":
            tmp.append(table2_col7[i]+"["+table2_col7[i+1]+"]")
            i+=2
        elif table2_col7[i]=="PubMed":
            tmp.append(table2_col7[i]+"["+"http://www.ncbi.nlm.nih.gov"+table2_col7_a[a_num]+"]")
            urllist.append("http://www.ncbi.nlm.nih.gov"+table2_col7_a[a_num])
            i+=1
            a_num+=1
        else:
            tmp.append(table2_col7[i])
            i+=1
    table2_col7 = tmp

    table2_col8 = x.xpath("//div[@id='_summary-evidence']//td[8]/text()")
    re_extract = re.compile('<td></td>')
    item_match = re.findall(re_extract, page.content)
    if item_match:
        tmp = [" ",]
    else:
        tmp=[]
    j=0
    re_extract = re.compile('</h5><p>(.*?)</p>')
    item_match = re.findall(re_extract, page.content)
    for i in range(len(table2_col8)):
        if table2_col8[i]=='not provided':
            tmp.append(table2_col8[i])
        else:
            tmp.append(item_match[j])
            j+=1
    table2_col8 = tmp
    
    
    for i in range(len(table2_col1)):
        table2[0].append(table2_col1[i])
        table2[1].append(table2_col2[i])
        table2[2].append(table2_col3[i])
        table2[3].append(table2_col4[i])
        table2[4].append(table2_col5[i])
        table2[5].append(table2_col6[i])
        table2[6].append(table2_col7[i])
        table2[7].append(table2_col8[i])
    table2 = DataFrame(table2).T
    table2.to_csv("/home/yindanping/gene/SearchGene/Searching/lib/tmpdata/table2",sep="\t",header=None)
    print urllist
    if flag[0].find("no conflicts")!=-1:
        return 0,urllist
    else :
        return 1,urllist


# In[ ]:

if __name__=="__main__":
    import sys
    url = "http://www.ncbi.nlm.nih.gov/clinvar/?term="+sys.argv[1]
    #try:
    a,b = get_table(url)
    print a
    print b
    #except :
    #    print "args error"

