# 一、项目概述

## 背景



## 技术栈
- requests
- beautifulsoup
- selenium

## 依赖包

```html
requests==2.26.0
bs4~=0.0.1
schedule==1.1.0
selenium~=3.141.0
beautifulsoup4~=4.6.3
Faker~=9.9.0
```

## 注意点

# 二、iptool.py

ip-tool文件在项目中实现的是一个IP池（类IpTool），基本思路是各代理网站上的免费代理并进行测试（因为网上的免费代理绝大部分都是不可用的），然后对外暴露一个random接口，并返回一个可用的代理（IP+端口）。

其中检测可用性的部分利用多线程实现。

# 三、answer.py

answer中有类CodeAnswer，CodeAnswer是项目中存储答案的类，其中有数据库名，题目编号，题解链接，题解类型和提取出的代码四个字段，并且CodeAnswer中实现了load_from_mongodb和save_to_mongodb两个方法，用于自动存入数据库和从数据库中取出答案。





# 四、sipder.py

spider中有类Spider，Spider是项目中爬虫的基类，其中利用自己写的IP池实现了random_proxy和random_header两大方法，之后写的爬虫只需要继承这个类则可以直接使用代理，专注于爬虫逻辑的编写而不需要再考虑使用代理的问题。




# 五、dotcpp_spider.py

## 概述

dotcpp_spider中有类DotCppSpider，基类为Spider，DotCppSpider实现了一个从模拟登陆，爬取答案，存储答案，从数据库加载答案，利用selenium在网页模拟提交答案的完整流程。



## 代码处理

### 代码提取

#### 1.pre标签 
pre class="brush:cpp;toolbar:false"

eg : [https://blog.dotcpp.com/a/8132](https://blog.dotcpp.com/a/8132)

一般是题解页面有专门的代码块的网页源码中都符合这一规则

#### 2.textarea标签 

textarea style="display:none;"

eg : [https://blog.dotcpp.com/a/1014](https://blog.dotcpp.com/a/1014)

也是有专门的代码块，但是没有pre标签，则整个题解的主要都包含在textarea标签中，需要进行清洗

注意，在这种格式下的

#### 3.div标签 

div class="ueditor_container"

eg : [https://blog.dotcpp.com/a/79843](https://blog.dotcpp.com/a/79843)

还有的题解页面没有代码块也没有textarea页面，这时题解的主要内容会放在一个div标签中

#### 4. text 和 string

对于就是标签内只有不含有其他标签子节点，那么这个 tag 可以使用 result.string 得到文本，也可以用 result.text 获得文本

如果 tag 包含了多个子节点，tag 就无法确定 result.string 方法应该调用哪个子节点的内容, result.string 的输出结果是 None

### 代码格式化

从网页源码中提取出的代码一般会有各种各样的问题，利用NBSP空格问题，还有中文字符等，在项目中我们主要是利用正则对其进行处理。

# 六、settings.py

settings在项目中主要是进行一些全局配置，在其他文件中只要引入这个文件并读取其中变量即可。



# 七、总结