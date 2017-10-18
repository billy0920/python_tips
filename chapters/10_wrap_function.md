## [Python笔记](https://billy0920.github.io/python_tips)
### Python学习总结——装饰函数
> 装饰函数，涉及到python的一个特殊语法：装饰器（@）。

以下的代码：
```python
@f1(arg)
@f2
def func(): pass
```
等价于：
```python
def func(): pass
func = f1(arg)(f2(func))
```
也就是说，@符号可以在函数前起到装饰的作用，对被装饰函数进行一次封装，从而大大简化代码的写作。@符号可以直接带一个函数名（用于装饰的函数），也可以带装饰函数跟装饰函数的参数。@可以叠加，其顺序是从最接近被装饰函数的装饰器开始解析，从下往上（这种教科书式的说法真是无趣）。

装饰函数，可以看作是第一个参数为被装饰函数的函数。我们可以定义一个用来记录函数执行记录的装饰函数：
```python
import datetime
def logged_func(func):
    def new_func():
        stime = datetime.datetime.now()
        print "%s"% stime
        ret = func()
        etime = datetime.datetime.now()
        print "%s"% etime
        print "cost time: %s" % (etime -stime)
        return ret
    return new_func

@logged_func
def test():
    for x in range(100):
        print x

if __name__ == "__main__":
    test()
```
上述例子中的装饰器，还没有支持对函数参数的解析，因此只能用于装饰未带参数的函数。要支持装饰带参数的函数，可以这样定义：
```python
import datetime
def logged_func(func):
    def new_func(*args, **keyword_args):
        stime = datetime.datetime.now()
        print "%s"% stime
        print "call function: %s, with args: %s, and keyword args: %s" % (func.__name__, args, keyword_args)
        ret = func(*args, **keyword_args)
        etime = datetime.datetime.now()
        print "%s"% etime
        print "cost time: %s" % (etime -stime)
        return ret
    return new_func

@logged_func
def test(a, b=10):
    for x in range(a):
        print x * b

if __name__ == "__main__":
    test(5)
```
装饰器返回的函数函的第一个*args是不带缺省值的参数列表，第二个参数**keyword_args是带缺省值的参数字典。通过这样的修改，这个装饰器可以用于任何参数（不管带不带参数，带不带缺省值参数），并且可以解析参数的名字和参数值等信息，已经具备了记录函数执行日志的基本功能。

但是这里还有一个问题，带有装饰器的函数已经不是原来的函数了，而是装饰器中定义的new_func，这个new_func跟被装饰的原函数的属性信息不同，在某些需要判断函数属性的情况下，容易导致出错。因此需要再添加一些代码，修改如下：
```python
import datetime


def logged_func(func):
    def new_func(*args, **keyword_args):
        stime = datetime.datetime.now()
        print "%s"% stime
        print "call function: %s, with args: %s, and keyword args: %s" % (func.__name__, args, keyword_args)
        ret = func(*args, **keyword_args)
        etime = datetime.datetime.now()
        print "%s"% etime
        print "cost time: %s" % (etime -stime)
        return ret

    for attr in dir(func):
        try:
            new_func.__setattr__(attr, func.__getattribute__(attr))
        except Exception, e:
            # print e, attr
            pass
    return new_func

@logged_func
def test(a, b=10):
    """test function doc."""
    for x in range(a):
        print x * b

if __name__ == "__main__":
    test(5)

```
因为有一些属性是不支持修改的，无法将被装饰函数的属性赋予装饰器返回的函数，因此在使用带装饰器的函数来说，确实是有一定的改变（本来就有改变）。有兴趣进一步了解的话，可以将异常捕获语句中的打印语句的注释去掉，就可以看到有哪些属性不能支持。通过以上的修改，在最大程度上还原了被装饰函数的属性。

#### 本质
> 装饰器的本质，是通过一个简洁的标注@来提供一个专门处理函数的函数。

装饰器函数接收函数及其参数列表作为输入，对被装饰函数进行处理，并返回一个函数定义。
实际上装饰器函数可以返回函数，也可以返回一个类，甚至可以返回任意类型的值。
理解了装饰器的本质，我们就可以利用装饰器来简化代码的编写，毕竟pythonic就是要多快好省地写代码。
但是我们也大可不必为了使用装饰器而专门写装饰器的代码，在必要的时候去使用它就可以了。
这个原则对于大部分的代码编写模式都是适用的。

猜测的约束：装饰器的使用是静态的。这个有点遗憾，如果能支持运行时动态使用就好了。
但是也没关系，从装饰器的本质看，这也仅仅是不能动态使用标注而已，直接调用装饰器函数的效果是一样的。

## [Python笔记](https://billy0920.github.io/python_tips)
