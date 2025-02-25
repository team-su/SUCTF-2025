# WP

![image-20250114152617853](https://gitee.com/xyqer/pic/raw/master/202501141526934.png)

观察模型合并部分，可以看出
$$
global\_model = global\_model + \sum_i^{10}(client\_model-global\_model)
$$
随着正常客户端的训练，其loss会越来越小，其模型与全局模型的差也会越来越小，当到了20epoch的时候就可以忽略不计，所以我们只需要正常训练一个含有后门且正常功能正常的模型，然后将模型减去全局模型后*10即可做到用自己的模型替换掉全局模型。

在训练自己模型的时候只需要将每个batch中部分图片变成后门数据然后训练即可。

