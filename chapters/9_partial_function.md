## [Python笔记](https://billy0920.github.io/python_tips)
### Python学习总结——偏函数
> 突然冒出这一篇，然而这篇文章介绍的内容，最能体现python的特点。

在python的functools中有一个partial函数，可以用于从一个函数生成一个新的函数。

网上有很多的例子，跟python的官方文档上的例子类似，都没能体现出这个偏函数的作用。基本的用法如下：
```python
from functools import partial
basetwo = partial(int, base=2)
basetwo('10010')
```

这段代码的意思是，用int()生成一个新的函数，设置int()的缺省参数base=2，这样，新的函数basetwo(x)相当于int(x, base=2)。

这个用途简直不要太无聊，概念难以理解，起的作用又可有可无。上面的例子，实际等效于如下的代码：
```python
basetwo = lambda x: int(x, base=2)
basetwo('10010')
```
这个写法更好理解，完全不超出原有的概念，效果也是完全一致的。

偏函数可以说是以上简化代码的一种泛化的实现，它提供一种统一的方式来实现生成偏函数，我们不需要额外定义匿名函数，也不需要为每个参数写特定的代码。虽然概念上有点奇怪，但是实际上还是很好用的。理解了它的等效函数的实现，也就能理解这个概念了。

## [Python笔记](https://billy0920.github.io/python_tips)
