#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Accommodation,User,Room
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math,datetime
from django.utils import timezone
from django.db.models import Q      #不要删除! myfun.obj_q_filter() 函数依赖
import json
import random
import myfun

'''
1.公寓、房间视图
'''
#公寓List  查询主页
def acc_list_view(request):
    #build_db_test()
    '''
    1.进行过滤,获得公寓集
    '''
    acc_filter_str = request.GET.get('acc_filter')
    city_list = []
    city_num = ""

    #排除城市输入错误
    try:
        city_num = int(request.GET.get('city'))
        city_list.append(myfun.CITY_LIST[city_num])
    except:
        pass
    acc_filter_list = []

    #排除房源过滤 输入错误
    if acc_filter_str not in ["None","",None,"undefined"]:
        acc_filter_list = acc_filter_str.split(',')

    filter_dict = {}
    filter_dict['address'] = city_list
    filter_dict['source_type'] = acc_filter_list

    Qfilter_str =  myfun.obj_q_filter("Accommodation",filter_dict)
    #print(Qfilter_str)

    accommodation_list = eval(Qfilter_str)
    count = eval(Qfilter_str).count()

    '''
    2.分页
    '''
    #我的分页
    page_count = int(math.ceil(float(count/12)))+1
    paginator = Paginator(accommodation_list, 12) # Show 25 contacts per page
    page = request.GET.get('page')
    if page != None and page != "undefined":    page=  int(page)
    else:   page = 1
    if page > page_count : page = page_count
    page_state = myfun.fen_ye(page,page_count)['page_state']
    ran_page = myfun.fen_ye(page,page_count)['ran_page']

    #Django 内置分页
    try:
        accommodation_list= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        accommodation_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        accommodation_list = paginator.page(paginator.num_pages)

    '''
    3.渲染模板
    '''
    session_email = request.session.get('email')
    user = None
    if session_email !=None:
        print "ac email_session:",session_email
        user = User.objects.get(email=session_email)
        session_email = 1
    #print(ran_page,page_count,page_state)
    return render(request, 'liwu/acc.html', {'accommodation_list':accommodation_list,
                                               'current_page':page,'page_count':page_count,'page_state':page_state,
                                               'ran_page':ran_page,'acc_filter_str':acc_filter_str,
                                             'session_email':session_email,"city_num":city_num,
                                             'user':user
                                               }
                  )

#公寓Detail 查询页面
def acc_detail(request,accommodation_id):
    acc = Accommodation.objects.get(pk = accommodation_id)
    #print(acc.name)
    session_email = request.session.get('email')
    print session_email
    user  = None
    if session_email!=None:
        try:
            print request.session.get('email')
            user = User.objects.get(email=unicode(session_email))
            session_email = 1
        except:
            del request.session['email']

    return render(request,"liwu/acc_detail.html",{'session_email':session_email,
                                                  'accommodation':acc,
                                                  'user':user
                                                  })

#用户视图 页面
def user_detail(request,user_id):
    visit = User.objects.get(id=user_id)
    session_email = request.session.get('email')
    publish_count = visit.accommodation_set.count()
    yourself = 0#鉴别访问用户页面的是否为本人
    user = None
    if unicode(session_email) == unicode(visit.email):
        print(session_email,visit.email)
        yourself = 1

    if session_email != None:
        user = User.objects.get(email= session_email)
        session_email  = 1

    return render(request,'liwu/user.html',{"user":user,"visit":visit,"session_email":session_email,
                                            "publish_count":publish_count,'yourself':yourself})

'''
2.注册与登录 分为渲染界面：返回html
            后台请求处理：返回json和设置session
'''
#注册登录界面
def reg_login(request):
    session_email = request.session.get('email')
    if session_email == None:
        return render(request,"liwu/reg_login.html")
    else:
        #pass
        #return render(request,"liwu/acc.html")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','acc'))

#登录验证 登录成功设置session
def login_json(request):
    email = request.POST['email']
    pw = request.POST['pw']
    try:
        user = User.objects.get(email = email,pw=pw)
        if user:
            request.session['email'] = email
            request.session.set_expiry(3600*24*7)
            return  HttpResponse(json.dumps({'msg':'y'}))
    except:
        return  HttpResponse(json.dumps({'msg':"n"}))

#注册验证
def register_json(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        email = request.POST['email']
        try:
            session_email = request.session.get('email')
            return  render(request,'liwu/acc')
        except:
            try:
                #用户是否存在
                user = User.objects.get(email = email)
                return  HttpResponse(json.dumps({'msg':'have_email'}))
            except:
                user = User(name = email, email = email, pw = pw)
                user.save()
                if user is not None:
                    return HttpResponse(json.dumps({'msg':'y'}))
                else:
                    return HttpResponse(json.dumps({'msg':'n'}))

#修改user请求
def edit_user(request):
    email = request.POST['email']
    sign = request.POST['sign']
   # print(email)
    user = User.objects.get(email=email)
    if user is not None:
        user.sign = sign
        user.save()
        return HttpResponse(json.dumps({'msg':'y'}))
    else:
        return HttpResponse(json.dumps({'msg':'n'}))

#注销请求
def logout(request):
    del request.session['email']
    return HttpResponse(json.dumps({'msg':'y'}))

