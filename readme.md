本项目为SUSTech 2022夏季学期 商业分析中的python应用 课程project，按照MIT License允许任意修改，传播。

与TIS交互，得到原始数据的部分参考了https://github.com/GhostFrankWu/SUSTech_Tools

# 作用？

1. 将tis上的数据copy到本地，方便操作
2. 调用了模糊查找的库( fuzzy_search.py #25)，找课程更加方便。教务系统中输入的课程名字必须是某课程名字的**连续子串**才会被匹配到。当然你也可以替换为其他模糊查找的库。
3. 自动根据想选的课程选择班级，使得能同时选上的课程数量最大。并且对于每个选到的课程，都给出https://nces.cra.moe/course  上的评分（如有）
4. 自动输出喵课脚本需要的Class.txt文件

# 怎么用？

确保tis上没有选课记录，否则可能搜不到想选的课程。（因为已经选过的课程不能再选）

关闭梯子

直接运行main.py



# 生成的文件

根据提示自动生成

raw_data.json -- 原始数据

alreadySelectedCourses.json -- tis上已经选了的课

courses.json --可以选的课

wishlist.json -- 待选的课程

selectedClass.json -- 脚本自动选择的班级



如果乱码请运行view_json.py



# 需要改进之处

1.不能处理tis上已经选过的课

2.通过随机算法选班级，因为不会遍历（
