# ktail族算法

**ktail系列算法用于从一个序列生成序列对应的有限状态自动机**。常见的用法是从日志中推断程序执行流。本库目前包含了该族算法的一个早期版本，参见论文：

+ Reiss, Steven P., and Manos Renieris. "Encoding program executions." Proceedings of the 23rd International Conference on Software Engineering. ICSE 2001. IEEE, 2001.

希望以后能有精力补上些新改进的实现吧。
![程序执行流]((https://github.com/zzkluck/KTailAlgorithm/blob/main/example_sequence/example.png))

## Prerequisites:
* python
* pyvis

## Installing:
1. Download the project code files with:

   `git clone https://github.com/zzkluck/KTailAlgorithm.git`

2. Go to the project directory

   `cd KTailAlgorithm`

## Usage:

To use the model, open a terminal, change directory to this project code, run the command: 

`python run.py`


## Project Structure:
1. run.py: 使用用例入口文件；
2. ktail.py: ktail算法的具体实现；

## Data Format:
* 测试用例来自某真实环境的日志数据，已经做过相关日志解析处理，原始的日志文本转换为日志模板序列，参见example_sequence\seq.csv。对于可能包含敏感信息的字段做了混淆/消去处理，但序列本身的特征还是保留下来了的。
