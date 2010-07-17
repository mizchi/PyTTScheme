#/usr/bin/python
#-*- encoding:utf-8 -*-
from pytyrant import PyTyrant
class TScheme(object) :
    def __init__(self,scheme,header=""):
        scheme["++unique++"]="int"
        self.__scheme = scheme
        self.quantity = 0
        self.header=header+":"
    
    def dump(self):
        self.__dump(self.__scheme)
        
    def __dump(self,scheme,header=""):
        for k,v in scheme.iteritems():
            if type(v)==dict :
                self.__dump(v,header+"/"+k)
            elif type(v) == str :
                print header+"/"+k+"\t"+v

    def raw_get(self,where="",number=-1):
        obj = {}
        query = self.header+"/"+where
        con = PyTyrant.open("localhost")
        ret = con.prefix_keys(query)
        for i in sorted(ret):
            if number==-1 or int(i.split("_")[-1]) == number :
                obj[i]=con[i]
        con.close()
        return obj
    
    def get(self,where="",number=-1):
        if type(where)==str : where = [where]
        objs=[]
        con = PyTyrant.open("localhost")
        ret = []
        for i in where :
            query = self.header+"/"+i
            ret += con.prefix_keys(query)
        for i in sorted(ret):
            ids=i.split("_")[-1]
            if number==-1 or ids == str(number) :
                item = self.__parse(i,con[i])
                item.update({"ids":ids})
                objs.append(item )
        con.close()
        return sorted(objs)
        
    def __parse(self,key,value):
        params = key.split("_")[0].split("/")[1:]
        item = self.__mkval(params,value)
        return item # self.__mkval(params,value)
        
    def put(self,dic,number=-1):
        if number == -1: number=self.get_length()
        
        dic["++unique++"]=str(number)
        con = PyTyrant.open("localhost")
        self.__put(dic,str(number),self.header)
        con.close()
        
    def __put(self,scheme,number,header=""):
        for k,v in scheme.iteritems():
            if type(v)==dict :
                self.__put(v,number,header+"/"+k)
            elif type(v) == str :
                query = header + "/" + k+"_"+number
                con = PyTyrant.open("localhost")
                con[query] = v
                con.close()
                
    def get_length(self):
        con = PyTyrant.open("localhost")
        query = self.header+"/"+"++unique++"
        length= len(con.prefix_keys(query))
        con.close()
        return length
        
    def __mkval(self,path,dic="val"):
        if not path:
            return dic
        else :
            ndic ={path[-1] :dic }
            return self.__mkval(path[0:-1],ndic)
            
    def delete_all(self):
        con=PyTyrant.open("localhost")
        ret = con.prefix_keys(self.header)
        for i in ret:
            del con[i]
        con.close()
                            
