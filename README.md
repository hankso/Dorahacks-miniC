# Dorahacks-miniC

2018.5.19 Dorahacks北航场

选了第一道题，实现mini的C词法分析器

两个思路：
- 使用python将C语言源文件替换成可以py解释器可以运行的文件：小成本小制作，复习了一遍C语言
- 将C语言源文件逐行处理，提取关键词（类型，运算符，保留字，变量名，函数名等），生成符号表，从符号表生成二叉树进行前序遍历得到重排序的符号表，将符号表写入文件使用lisp可直接运行

第二种方案实例：
- 源代码：`a = a + b * (c / d)`
- 符号表：`["a", "=", "a", "+", "b", "*", "(", "c", "/", "d", ")"]`
- 重排序：`["=", "a", ["+", "a", ["*", "b", ["/", "c", "d"]]]]`
- 存为rst.lisp: `(setq a (+ a (* b (/ c d))))`
