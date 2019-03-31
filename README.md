# doubanSpider

1.项目通过scrapy框架进行豆瓣信息爬取
2.通过模拟post请求进行模拟登陆获取cookie，编写transToDict函数将cookie进行格式化处理
3.设置随机请求头User-Agent
4.通过重写start_requests对多页面信息进行爬取
5.重写pipeline,对字段过长的信息进行截取，当超过100字时省略后面的字符且添加...代替
6.将数据通过isinstance函数进行mysql分表存储（有多个item）
