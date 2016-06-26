# Create your views here.
#coding: utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#import django.views.decorators.csrf.csrf_token
#from django.template.context_processors import csrf
#from django.template import RequestContext
import os
import json
from django.shortcuts import render_to_response
from .forms import SearchForm1,SearchForm2,SearchForm3
from django.http import HttpResponse

#import get_table
# Create your views here.

def index(request):
    return render(request,"index.html")
def display(request):
    return render(request,"hgvs_display.html")


def searchhgvs(request):
    if 'hgvs' in request.GET and request.GET['hgvs']:
        hg=request.GET['hgvs']
        cmd="/usr/bin/python /home/yindanping/gene/SearchGene/Searching/lib/get_table.py "+hg
        os.system(cmd)       
        form = SearchForm1()
        return render_to_response('hgvs_display.html',{'form': form})

    else:
        form = SearchForm1()
    return render_to_response('hgvs.html', {'form': form})

def hgvs_display1(request):
    file1=open("/home/yindanping/gene/SearchGene/Searching/lib/tmpdata/table1",'r').readlines()
    t1=[]
    for line in file1:
        d=dict()
        item1=line.strip().split('\t')
        d['Cs']=item1[0]
        d['Rs']=item1[1]
        d['Cm']=item1[2]
        d['Con']=item1[3]
        d['Orign']=item1[4]
        d['Cita']=item1[5]
        d['SSn']=item1[6]
        d['Sa']=item1[7]
        t1.append(d)
    return HttpResponse(json.dumps(t1, ensure_ascii=False))

def hgvs_display2(request):
    file2=open("/home/yindanping/gene/SearchGene/Searching/lib/tmpdata/table2",'r').readlines()
    t2=[]
    for line in file2:
        d=dict()
        item2=line.strip().split('\t')
        d['Sub']=item2[0]
        d['Fam']=item2[1]
        d['Ind']=item2[2]
        d['Ao']=item2[3]
        d['Eth']=item2[4]
        d['Go']=item2[5]
        d['CD']=item2[6]
        d['De']=item2[7]
        t2.append(d)
    return HttpResponse(json.dumps(t2, ensure_ascii=False))

def searchsymbol(request):
    if 'symbol' in request.GET and request.GET['symbol']:
        sy=request.GET['symbol']
    else:
        form = SearchForm2()
    return render_to_response('symbol.html', {'form': form})

def searchmedicine(request):
    if 'medicine' in request.GET and request.GET['medicine']:
        med=request.GET['medicine']
    else:
        form = SearchForm3()
    return render_to_response('medicine.html', {'form': form})

def TextAnalyse(request):
    if 'text' in request.GET and request.GET['text']:
        text=request.GET['text']
    else:
        form = SearchForm3()
    return render_to_response('text.html', {'form': form})
        
    return HttpResponse("Success!!!")

