#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Created on 2017-5-26 by Author:GuoLikai

from Stark import settings
import time,json
import copy
class DataStore(object):
    '''
    processing the client reported service data , do some data optimiaztion and save it into redis DB
    '''
    def __init__(self, client_id,service_name, data,redis_obj):
        '''
        :param client_id:
        :param service_name:
        :param data: the client reported service clean data ,
        :return:
        '''
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.redis_conn_obj = redis_obj
        self.process_and_save()

    def get_data_slice(self,lastest_data_key,optimization_interval):
        '''
        :param optimization_interval: e.g: 600, means get latest 10 mins real data from redis
        :return:
        '''
        #取Redis列表中所有数据
        all_real_data = self.redis_conn_obj.lrange(lastest_data_key,1,-1)
        #print("get data range of:",lastest_data_key)
        data_set = []
        for item in all_real_data:
            item = item.decode()
            #print(json.loads(item))
            data  = json.loads(item)
            if len(data) ==2:
                #print("real data item:",data[0],data[1])
                service_data, last_save_time = data
                #print(time.time()- last_save_time, optimization_interval)
                if time.time() - last_save_time <= optimization_interval:# filter this data point out
                    #print(time.time()- last_save_time, optimization_interval)
                    data_set.append(data)
        #print("--->data set",data_set)
        return data_set
    def process_and_save(self):
        '''
        processing data and save into redis
        :return:
        '''
        print("\033[42;1m----service data optimize & save----\033[0m")
        #print( self.client_id,self.service_name,self.data)
        if self.data['status'] == 0:# service data is valid
            for key,data_series_val in settings.STATUS_DATA_OPTIMIZATION.items():
                data_series_key_in_redis = "StatusData_%s_%s_%s" %(self.client_id,self.service_name,key)
                #Redis里对应的列表名：data_series_key_in_redis；
                #print(data_series_key_in_redis,data_series_val)
                last_point_from_redis = self.redis_conn_obj.lrange(data_series_key_in_redis,-1,-1)  #lrange()函数取Redis列表；取最后一个值；
                if not last_point_from_redis: #this key is not exist in redis
                    #so initialize a new key ,the first datar point in the data set will only be used to identify that when was \
                    #the data got saved last time
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([None,time.time()] ))  #第一次初始化数据
                if data_series_val[0] == 0:#this dataset is for unoptimized data, only the latest data no need optimiaztion
                    #代表最新获取的数据，不需要优化；
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([self.data, time.time()]))
                else: #data might needs to be optimized
                    #print("*****>>",self.redis_conn_obj.lrange(data_series_key_in_redis,-2,-1))
                    #last_point_data,last_point_save_time =  json.loads(self.redis_conn_obj.lrange(data_series_key_in_redis,-2,-1)[0])
                    last_point_data,last_point_save_time = json.loads(self.redis_conn_obj.lrange(data_series_key_in_redis,-2,-1)[0].decode()) #bytes转换str
                    if time.time() - last_point_save_time >= data_series_val[0]: # reached the data point update interval ,
                        lastest_data_key_in_redis = "StatusData_%s_%s_latest" % (self.client_id,self.service_name)
                        print(u"Redis数据库优化存储的Key:\033[31;1m %s \033[0m" % data_series_key_in_redis )
                        #最近n分钟的数据，已经取到了放进data_set中；
                        data_set = self.get_data_slice(lastest_data_key_in_redis,data_series_val[0])
                        #print(u"需优化的数据个数:",len(data_set))
                        if len(data_set) > 0:
                            optimized_data = self.get_optimized_data(data_series_key_in_redis, data_set)
                            print('get_optimized_data ok')
                            if optimized_data:
                                self.save_optimized_data(data_series_key_in_redis, optimized_data)
                                print(u'-->数据优化存储OK')
        else:
            print("report data is invalid::",self.data)
            raise ValueError

    def save_optimized_data(self,data_series_key_in_redis, optimized_data):
        '''
        save the optimized data into db
        :param optimized_data:
        :return:
        '''
        self.redis_conn_obj.rpush(data_series_key_in_redis, json.dumps([optimized_data, time.time()])   )
    def get_optimized_data(self,data_set_key, raw_service_data):
        '''
        calculate out ava,max,minum,mid value from raw service data set
        :param data_set_key: where the optimized data needed to save to in redis db
        :param raw_service_data: raw service data data list
        :return:
        '''
        #获取优化后的数据
        #index_init =[avg,max,min,mid]
        #print("get_optimized_data:",raw_service_data[0] )
        service_data_keys = raw_service_data[0][0].keys()   #[iowait,ststem,idle...]
        first_service_data_point = raw_service_data[0][0] # use this to build up a new empty dic
        #print(u"需优化数据分类:",service_data_keys)
        optimized_dic = {} #set a empty dic, will save optimized data later
        if 'data' not  in service_data_keys: #means this dic has  no subdic, works for service like cpu,memory
            for key in service_data_keys:
                optimized_dic[key] = []
            #optimized_dic = optimized_dic.fromkeys(first_service_data_point,[])
            tmp_data_dic = copy.deepcopy(optimized_dic)  #为了临时存最近几分钟的数据，
            #把他们按照每个指标都搞成一个列表,来存取最近n分钟的数据；
            #print("tmp data dic:",tmp_data_dic)
            for service_data_item,last_save_time in raw_service_data:  #loop 最近n分钟的数据
                #print(service_data_item)
                for service_index,v in service_data_item.items():   #loop每个数据点的指标
                    #print(service_index,v)
                    tmp_data_dic[service_index].append(round(float(v),2)) #把这个点的数据放到临沭列表中
                #print(service_data_item,last_save_time)
            for service_k,v_list in tmp_data_dic.items():
                #print(service_k, v_list)
                avg_res = self.get_average(v_list)
                max_res = self.get_max(v_list)
                min_res = self.get_min(v_list)
                mid_res = self.get_mid(v_list)
                optimized_dic[service_k]= [avg_res,max_res,min_res,mid_res]
                #print("优化后单项数据"，service_k, optimized_dic[service_k])

        else: # has sub dic inside key 'data', works for a service has multiple independent items, like many ethernet,disks...
            #print("**************>>>",first_service_data_point )
            for service_item_key,v_dic in first_service_data_point['data'].items():
                #service_item_key相当于lo，eth0；v_dic 相当于{'t_in':111,'t_out':444}
                optimized_dic[service_item_key] = {}
                for k2,v2 in v_dic.items():
                    optimized_dic[service_item_key][k2] = []   #{eth0:{t_in:[]},eth0:{t_out:[]}}
            tmp_data_dic = copy.deepcopy(optimized_dic)
            if tmp_data_dic: #some times this tmp_data_dic might be empty due to client report err
                #print('-->tmp_data_dic:', tmp_data_dic)
                for service_data_item,last_save_time in raw_service_data: #loop 最近n分钟的数据
                    for service_index,val_dic in service_data_item['data'].items():
                        #print(service_index,val_dic)
                        #service_index相当于lo，eth0；
                        for service_item_sub_key, val in val_dic.items():
                            #service_item_sub_key相当于t_in,t_out
                            #if service_index == 'lo':
                            #print(service_index,service_item_sub_key,val)
                            tmp_data_dic[service_index][service_item_sub_key].append(round(float(val),2))

                for service_k,v_dic in tmp_data_dic.items():
                    for service_sub_k,v_list in v_dic.items():
                        #print(service_k, service_sub_k, v_list)
                        avg_res = self.get_average(v_list)
                        max_res = self.get_max(v_list)
                        min_res = self.get_min(v_list)
                        mid_res = self.get_mid(v_list)
                        optimized_dic[service_k][service_sub_k] = [avg_res,max_res,min_res,mid_res]
                        #print(u"-->优化后数据：",service_k, service_sub_k, optimized_dic[service_k][service_sub_k])
            else:
                print("\033[41;1mMust be sth wrong with client report data\033[0m")
        print(u"-->优化后的数据:", optimized_dic)
        return optimized_dic

    def get_average(self,data_set):
        '''
        calc the avg value of data set
        :param data_set:
        :return:
        '''
        if len(data_set) > 0:
            return sum(data_set) /len(data_set)
            #//表示不余数；
        else:
            return 0
    def get_max(self,data_set):
        '''
        calc the max value of the data set
        :param data_set:
        :return:
        '''
        if len(data_set) > 0:
            return max(data_set)
        else:
            return 0
    def get_min(self,data_set):
        '''
        calc the minimum value of the data set
        :param data_set:
        :return:
        '''
        if len(data_set) > 0:
            return min(data_set)
        else:
            return 0
    def get_mid(self,data_set):
        '''
        calc the mid value of the data set
        :param data_set:
        :return:
        '''
        if len(data_set) > 0:
            data_set.sort()
            #import math #Python之向上取整math.ceil、向下取整floor以及四舍五入round
            #dataindex = math.ceil(len(data_set)/2)
            #print(dataindex)
            return data_set[len(data_set)//2]
        else:
            return 0