#coding:utf-8
from .models import  User,Accommodation,Room
from django.utils import timezone
import random,datetime

CITY_LIST = [u'伯明翰',u'格拉斯哥',u'贝尔法斯特',u'伦敦',u'曼彻斯特',u'利兹',u'利物浦',u'卡迪夫',u'爱丁堡',u'布里斯托']
'''
功能：生成10个用户，每个用户发布20~60个公寓，每个公寓产生2~8个房间。其中地址，房源类型，房间类型 这3个字段随机生成。
0.此函数不要初始化多次，再次初始化需要把数据库清0，否则出现重复id，引发错误.清除数据库:python manage.py flush
1.可以通过shell方式 和在views中使用此函数进行随机构建数据填充数据库。
'''

def build_db_test():
    for iuser in xrange(1,11):
        name='user_%s' % iuser
        user = User(name=name, email="%s@ding.com" % name, pw="1",)
        user.save()
        ran_acc_num = random.randint(20,60)

        for iacc in xrange(1,ran_acc_num+1):
             acc_choices = Accommodation.SOURCE_TYPE_CHOICES
             acc_name = 'Accommodation_%s' % ((iuser-1)*10+iacc)
             acc = Accommodation(name = acc_name,
                                 user_publish = user,
                                 publish_username = user.name,
                                 address=(random.choice(CITY_LIST)),
                                 source_type=random.choice(acc_choices)[0],
                           )
             acc.save()
             ran_room_num = random.randint(2,8)
             for iroom in xrange(1,ran_room_num+1):
                 room_choices =Room.SOURCE_TYPE_CHOICES
                 week_price = random.randint(150,400)
                 order_price = week_price + random.randint(50,200)
                 room = Room(name='%s_room_%s'%(acc_name,iroom),
                             bathroom = random.choice([True,False]),
                             accommodation=acc,
                             week_price = week_price,
                             order_price = order_price,
                             deposit = order_price,
                             start_data= timezone.now()-datetime.timedelta(days=-200),
                             end_data = timezone.now()-datetime.timedelta(days=-565),
                             source_type= random.choice(room_choices)[0]
                        )
                 room.save()
    print(u"数据构建完成！")


#用Q对象查询和eval()方法 第一版 进行多选过滤 无连续过滤
def obj_q_filter_test(obj_str,type,filter_list):

    len_filter = len(filter_list)
    if len_filter == 0:
        obj_list = eval(obj_str).objects.all()
        obj_count = eval(obj_str).objects.count()
        return (obj_list,obj_count)
    filter_strs = ""
    for filter in filter_list:
        filter_strs += "Q(%s='%s')|"%(type,filter)
    eval_str = "%s.objects.filter(%s)"%(obj_str,filter_strs[:-1])
    obj_list = eval(eval_str)
    return  (obj_list,obj_list.count())

'''
利用Q对象进行过滤，可以实现连续过滤
Parameter:
    obj_str = Food
    filter_dict = {"fruit":["apple","banana"],
                    "drink":["cola","beer","tea"]
                   }
Return a str: Food.objects.filter(Q(fruit='apple')|Q(fruit='banana')).filter(Q(drink='cola')|Q(drink='beer')|Q(drink='tea'))
'''
def obj_q_filter(obj_str,filter_dict):
    return_str = ""
    for key in filter_dict.keys():
        filter_strs = ""
        if filter_dict[key] != None and len(filter_dict[key]) != 0:#为空跳过
            for filter in filter_dict[key]:
                if filter!=None and filter != "undefined" and len(filter) != 0:#[]中的选项不为空
                    filter_strs += "Q(%s='%s')|"%(key,filter)
            return_str += ".filter("+ filter_strs[:-1]+")"#-1 为去掉最后一个 "|" 符号
    if len(return_str) > 0:
        eval_str = "%s.objects%s"%(obj_str,return_str)
        return  eval_str
    else:
        return "%s.objects.all()" % obj_str

'''
Q函数测试
'''
obj_str = "Accommodation"
filter_dict=  {}
filter_dict['address'] = [u'伦敦',u'爱丁堡']
filter_dict['source_type'] = ["AP","None"]
obj_str = "Food"
filter_dict = {"fruit":["apple","banana"],
                "drink":["cola","beer","tea"]
               }
filter_dict = {"fruit":["apple"],}

#print(obj_q_filter(obj_str,filter_dict))

'''
:param  page_state       "0_0": 无左省略号，无右省略号
                         "0_1": 无左省略号，有右省略号
                         "1_0"：有左省略号，无右省略号
                         "1_1"：有左省略号, 有右省略号
'''
def fen_ye(page,page_count):

    ret_dict = {}
    ran_page = []
    page_state = "0_0"
    size = 7#显示6页
    aside = 3

    if page == page_count and page == 1:
        ret_dict['page_state'] = "0_0"
        ret_dict['ran_page'] = range(1,2)
        return  ret_dict

    if page_count < size:   #最大页小于7  显示全部页面无左右省略号----0_0
        ran_page = range(1,page_count+1);
    elif page_count - page <3 :    #最大页=当前页,且都大于7  倒数显示（7） 页 由左省略号，无右省略号----1_0
        ran_page = range(page-4,page_count+1)
        page_state = "1_0"
    elif page <7: #最大页大于7，当前页小于7， 显示到7页 ，无左省略号，有省略号 0_1
    #elif 7-page < 3:
        ran_page = range(1,7+1)
        page_state = "0_1"
    else:
        ran_page = range(page-3,page+4) #当前页与最大页都大于7 左右两边各显示3页 有左右省略号----- 1_1
        page_state = "1_1"
    ret_dict['ran_page'] = ran_page
    ret_dict['page_state'] = page_state

    return ret_dict

'''
分页函数测试
'''
# print(fen_ye(1,10))
# print(fen_ye(4,10))
# print(fen_ye(8,10))
# for i in range(1,3):
#     print(i,fen_ye(i,3))


