"""
Python 知识闯关小游戏
纯原生 Python 实现，仅使用 input/print，不引入任何第三方库。
题库涵盖变量赋值、运算符、字符串、列表、循环、字典等核心知识点。
排行榜使用 JSON 文件持久化存储。
"""

import json
import os
import random

# ==================== 题库定义 ====================

# 简单题（15题）：变量赋值、print输出、基础运算符、type()、字符串基础
EASY_QUESTIONS = [
    {
        "question": "以下代码的输出结果是什么？\nx = 10\nprint(x)",
        "options": ["A) 10", "B) x", "C) '10'", "D) 报错"],
        "answer": "A",
        "hint": "x 被赋值为整数 10，print(x) 会输出变量的值 10。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(type(3.14))",
        "options": ["A) <class 'int'>", "B) <class 'float'>", "C) <class 'str'>", "D) <class 'bool'>"],
        "answer": "B",
        "hint": "3.14 是浮点数，对应 float 类型。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(2 + 3 * 4)",
        "options": ["A) 20", "B) 14", "C) 24", "D) 9"],
        "answer": "B",
        "hint": "Python 遵循数学运算优先级，先乘除后加减：3*4=12，2+12=14。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(10 // 3)",
        "options": ["A) 3.33", "B) 3", "C) 4", "D) 1"],
        "answer": "B",
        "hint": "// 是整除运算符，10 // 3 = 3，只保留整数部分，向下取整。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(10 % 3)",
        "options": ["A) 3", "B) 1", "C) 0", "D) 3.33"],
        "answer": "B",
        "hint": "% 是取余运算符，10 除以 3 商 3 余 1，所以结果是 1。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(type('hello'))",
        "options": ["A) <class 'int'>", "B) <class 'list'>", "C) <class 'str'>", "D) <class 'float'>"],
        "answer": "C",
        "hint": "用单引号或双引号括起来的内容是字符串（str）类型。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(type(True))",
        "options": ["A) <class 'int'>", "B) <class 'str'>", "C) <class 'true'>", "D) <class 'bool'>"],
        "answer": "D",
        "hint": "True 是布尔值，对应 bool 类型。注意首字母大写。"
    },
    {
        "question": "以下代码的输出结果是什么？\na = 5\nb = a\nprint(b)",
        "options": ["A) a", "B) 5", "C) 'b'", "D) 报错"],
        "answer": "B",
        "hint": "b = a 将 a 的值 5 赋给 b，所以 print(b) 输出 5。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(2 ** 3)",
        "options": ["A) 6", "B) 5", "C) 8", "D) 9"],
        "answer": "C",
        "hint": "** 是幂运算符，2 ** 3 表示 2 的 3 次方，即 2*2*2=8。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint('Py' + 'thon')",
        "options": ["A) Py thon", "B) Python", "C) Py+thon", "D) 报错"],
        "answer": "B",
        "hint": "+ 运算符可以拼接字符串，'Py' + 'thon' 结果为 'Python'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(3 * 'ha')",
        "options": ["A) 3ha", "B) hahaha", "C) ha3", "D) 报错"],
        "answer": "B",
        "hint": "字符串乘以整数 n 会将字符串重复 n 次，3 * 'ha' = 'hahaha'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(type(42))",
        "options": ["A) <class 'int'>", "B) <class 'float'>", "C) <class 'str'>", "D) <class 'number'>"],
        "answer": "A",
        "hint": "42 是整数，对应 int（integer）类型。"
    },
    {
        "question": "以下代码的输出结果是什么？\nname = 'Alice'\nprint(name[0])",
        "options": ["A) A", "B) l", "C) Alice", "D) 报错"],
        "answer": "A",
        "hint": "字符串可以通过索引访问单个字符，索引从 0 开始，name[0] 是 'A'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(len('Python'))",
        "options": ["A) 5", "B) 6", "C) 7", "D) 4"],
        "answer": "B",
        "hint": "len() 函数返回字符串的长度，'Python' 有 6 个字符。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(int('123') + 1)",
        "options": ["A) 1231", "B) 124", "C) '124'", "D) 报错"],
        "answer": "B",
        "hint": "int('123') 将字符串 '123' 转为整数 123，再加 1 等于 124。"
    },
]

# 中等题（15题）：if判断、for循环、字符串切片、列表基础操作、range()
MEDIUM_QUESTIONS = [
    {
        "question": "以下代码的输出结果是什么？\nfor i in range(3):\n    print(i, end=' ')",
        "options": ["A) 0 1 2 ", "B) 1 2 3 ", "C) 0 1 2 3 ", "D) 1 2 "],
        "answer": "A",
        "hint": "range(3) 生成 0, 1, 2 三个数（不包含 3），end=' ' 使输出以空格分隔。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint('Python'[1:4])",
        "options": ["A) Pyth", "B) yth", "C) ytho", "D) Pyt"],
        "answer": "B",
        "hint": "切片 [1:4] 取索引 1 到 3 的字符（不包含 4），即 'y', 't', 'h'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nfruits = ['apple', 'banana', 'cherry']\nprint(fruits[1])",
        "options": ["A) apple", "B) banana", "C) cherry", "D) 报错"],
        "answer": "B",
        "hint": "列表索引从 0 开始，fruits[0]='apple'，fruits[1]='banana'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [1, 2, 3]\nnums.append(4)\nprint(len(nums))",
        "options": ["A) 3", "B) 4", "C) 5", "D) 报错"],
        "answer": "B",
        "hint": "append() 在列表末尾添加一个元素，添加后列表变为 [1,2,3,4]，长度为 4。"
    },
    {
        "question": "以下代码的输出结果是什么？\nx = 15\nif x > 10:\n    print('big')\nelse:\n    print('small')",
        "options": ["A) big", "B) small", "C) big small", "D) 报错"],
        "answer": "A",
        "hint": "15 > 10 为 True，执行 if 分支，输出 'big'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(list(range(1, 5)))",
        "options": ["A) [1, 2, 3, 4, 5]", "B) [1, 2, 3, 4]", "C) [0, 1, 2, 3, 4]", "D) [0, 1, 2, 3]"],
        "answer": "B",
        "hint": "range(1, 5) 生成从 1 到 4 的整数序列（不包含 5）。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint('hello'[::-1])",
        "options": ["A) hello", "B) olleh", "C) h", "D) o"],
        "answer": "B",
        "hint": "[::-1] 是字符串反转的常用写法，步长为 -1 表示从后往前取。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [3, 1, 2]\nnums.sort()\nprint(nums)",
        "options": ["A) [3, 1, 2]", "B) [1, 2, 3]", "C) [2, 1, 3]", "D) [3, 2, 1]"],
        "answer": "B",
        "hint": "sort() 方法对列表进行原地升序排序，结果为 [1, 2, 3]。"
    },
    {
        "question": "以下代码的输出结果是什么？\nfor i in range(0, 10, 3):\n    print(i, end=' ')",
        "options": ["A) 0 3 6 9 ", "B) 0 3 6 ", "C) 3 6 9 ", "D) 0 1 2 3 "],
        "answer": "A",
        "hint": "range(0, 10, 3) 从 0 开始，步长为 3，生成 0, 3, 6, 9（9 < 10）。"
    },
    {
        "question": "以下代码的输出结果是什么？\na = [1, 2, 3]\nprint(a + [4, 5])",
        "options": ["A) [1, 2, 3, 4, 5]", "B) [5, 4, 3, 2, 1]", "C) [10]", "D) 报错"],
        "answer": "A",
        "hint": "+ 运算符可以将两个列表拼接成一个新列表。"
    },
    {
        "question": "以下代码的输出结果是什么？\nx = 7\nif x % 2 == 0:\n    print('偶数')\nelif x % 3 == 1:\n    print('余1')\nelse:\n    print('其他')",
        "options": ["A) 偶数", "B) 余1", "C) 其他", "D) 偶数 余1"],
        "answer": "B",
        "hint": "7 % 2 = 1 不等于 0，跳过 if；7 % 3 = 1 等于 1，匹配 elif，输出 '余1'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint('abc' * 2 + 'd')",
        "options": ["A) abcabcd", "B) abcdabcd", "C) abcabc d", "D) abc2d"],
        "answer": "A",
        "hint": "'abc' * 2 = 'abcabc'，再拼接 'd'，结果为 'abcabcd'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [10, 20, 30, 40]\nprint(nums[1:3])",
        "options": ["A) [10, 20]", "B) [20, 30]", "C) [20, 30, 40]", "D) [10, 20, 30]"],
        "answer": "B",
        "hint": "列表切片 [1:3] 取索引 1 和 2 的元素，即 [20, 30]。"
    },
    {
        "question": "以下代码的输出结果是什么？\ns = 'Hello World'\nprint(s.split())",
        "options": ["A) ['Hello', 'World']", "B) ['HelloWorld']", "C) 'Hello World'", "D) ['H', 'e', 'l', 'l', 'o']"],
        "answer": "A",
        "hint": "split() 默认按空格分割字符串，返回列表 ['Hello', 'World']。"
    },
    {
        "question": "以下代码的输出结果是什么？\nfor i in range(5):\n    if i == 3:\n        break\n    print(i, end=' ')",
        "options": ["A) 0 1 2 ", "B) 0 1 2 3 ", "C) 0 1 2 3 4 ", "D) 3 "],
        "answer": "A",
        "hint": "break 在 i==3 时跳出循环，所以只输出 0, 1, 2。"
    },
]

# 困难题（15题）：while循环、列表推导式、嵌套循环、字典操作、综合题
HARD_QUESTIONS = [
    {
        "question": "以下代码的输出结果是什么？\nprint([x**2 for x in range(5)])",
        "options": ["A) [0, 1, 4, 9, 16]", "B) [1, 4, 9, 16, 25]", "C) [0, 1, 2, 3, 4]", "D) [1, 2, 3, 4, 5]"],
        "answer": "A",
        "hint": "列表推导式对 range(5) 即 0,1,2,3,4 中的每个 x 计算 x**2，结果为 [0,1,4,9,16]。"
    },
    {
        "question": "以下代码的输出结果是什么？\nd = {'a': 1, 'b': 2, 'c': 3}\nprint(d['b'])",
        "options": ["A) 1", "B) 2", "C) 3", "D) 'b'"],
        "answer": "B",
        "hint": "通过键访问字典值，d['b'] 返回键 'b' 对应的值 2。"
    },
    {
        "question": "以下代码的输出结果是什么？\nresult = 0\ni = 1\nwhile i <= 4:\n    result += i\n    i += 1\nprint(result)",
        "options": ["A) 6", "B) 10", "C) 4", "D) 15"],
        "answer": "B",
        "hint": "while 循环累加：1+2+3+4=10。i 从 1 增加到 5 时条件不满足，退出循环。"
    },
    {
        "question": "以下代码的输出结果是什么？\nfor i in range(3):\n    for j in range(2):\n        print('*', end='')\n    print()",
        "options": ["A) **\\n**\\n**\\n", "B) ***\\n***\\n", "C) **\\n**\\n", "D) *\\n*\\n*\\n"],
        "answer": "A",
        "hint": "外层循环 3 次，每次内层循环打印 2 个 '*'，然后 print() 换行。"
    },
    {
        "question": "以下代码的输出结果是什么？\nd = {'x': 1, 'y': 2}\nd['z'] = 3\nprint(len(d))",
        "options": ["A) 2", "B) 3", "C) 4", "D) 报错"],
        "answer": "B",
        "hint": "d['z'] = 3 向字典添加新键值对，字典变为 {'x':1,'y':2,'z':3}，长度为 3。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint([i for i in range(10) if i % 3 == 0])",
        "options": ["A) [0, 3, 6, 9]", "B) [3, 6, 9]", "C) [0, 3, 6]", "D) [1, 2, 3]"],
        "answer": "A",
        "hint": "带条件的列表推导式，筛选 range(10) 中能被 3 整除的数：0, 3, 6, 9。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [1, 2, 3, 4, 5]\nprint(nums[-2])",
        "options": ["A) 2", "B) 3", "C) 4", "D) 5"],
        "answer": "C",
        "hint": "负索引从末尾开始计数，-1 是最后一个元素(5)，-2 是倒数第二个(4)。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint(list('abc'))",
        "options": ["A) 'abc'", "B) ['a', 'b', 'c']", "C) ['abc']", "D) (a, b, c)"],
        "answer": "B",
        "hint": "list() 将字符串转换为字符列表，每个字符成为列表的一个元素。"
    },
    {
        "question": "以下代码的输出结果是什么？\nd = {'a': 1, 'b': 2}\nprint(list(d.keys()))",
        "options": ["A) [1, 2]", "B) ['a', 'b']", "C) ['a:1', 'b:2']", "D) [('a', 1), ('b', 2)]"],
        "answer": "B",
        "hint": "d.keys() 返回字典所有键的视图对象，转为列表后为 ['a', 'b']。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [1, 2, 3, 2, 1]\nprint(nums.count(2))",
        "options": ["A) 1", "B) 2", "C) 3", "D) 5"],
        "answer": "B",
        "hint": "count() 方法返回元素在列表中出现的次数，2 出现了 2 次。"
    },
    {
        "question": "以下代码的输出结果是什么？\nx = 0\nwhile x < 5:\n    x += 1\n    if x == 3:\n        continue\n    print(x, end=' ')",
        "options": ["A) 1 2 3 4 5 ", "B) 1 2 4 5 ", "C) 0 1 2 4 5 ", "D) 1 2 3 4 "],
        "answer": "B",
        "hint": "continue 跳过当前迭代的剩余代码。当 x==3 时跳过 print，所以不输出 3。"
    },
    {
        "question": "以下代码的输出结果是什么？\nprint({x: x*2 for x in range(3)})",
        "options": ["A) {0: 0, 1: 2, 2: 4}", "B) {1: 2, 2: 4, 3: 6}", "C) {0: 2, 1: 4, 2: 6}", "D) 报错"],
        "answer": "A",
        "hint": "字典推导式：range(3) 生成 0,1,2，键为 x，值为 x*2。"
    },
    {
        "question": "以下代码的输出结果是什么？\nnums = [3, 1, 4, 1, 5]\nprint(sorted(set(nums)))",
        "options": ["A) [3, 1, 4, 1, 5]", "B) [1, 1, 3, 4, 5]", "C) [1, 3, 4, 5]", "D) [5, 4, 3, 1]"],
        "answer": "C",
        "hint": "set(nums) 去重得到 {1,3,4,5}，sorted() 排序后为 [1,3,4,5]。"
    },
    {
        "question": "以下代码的输出结果是什么？\nfor i in range(1, 4):\n    print(str(i) * i)",
        "options": ["A) 1\\n22\\n333", "B) 1\\n2\\n3", "C) 11\\n222\\n3333", "D) 1\\n22\\n333\\n"],
        "answer": "A",
        "hint": "str(i)*i 将数字转为字符串后重复 i 次：'1'*1='1', '2'*2='22', '3'*3='333'。"
    },
    {
        "question": "以下代码的输出结果是什么？\nd = {'a': 1, 'b': 2, 'c': 3}\ndel d['b']\nprint(len(d))",
        "options": ["A) 1", "B) 2", "C) 3", "D) 报错"],
        "answer": "B",
        "hint": "del d['b'] 删除键为 'b' 的键值对，字典变为 {'a':1,'c':3}，长度为 2。"
    },
]

# ==================== 排行榜文件路径 ====================
LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")


# ==================== 显示函数 ====================

def show_banner():
    """显示游戏横幅"""
    print()
    print("╔══════════════════════════════════════╗")
    print("║     Python 知识闯关挑战赛            ║")
    print("║     测试你的 Python 功底！           ║")
    print("╚══════════════════════════════════════╝")
    print()


def show_menu():
    """显示主菜单"""
    print("========== Python 知识闯关 ==========")
    print("  1. 开始游戏")
    print("  2. 查看排行榜")
    print("  0. 退出游戏")
    print("======================================")


def show_status(level, hp, score):
    """显示当前状态（关卡、生命值、积分）"""
    hearts = "♥" * hp + "♡" * (3 - hp)
    print(f"\n[ 关卡 {level} ]  生命值: {hearts}  积分: {score}")
    print("-" * 36)


# ==================== 排行榜函数 ====================

def load_leaderboard():
    """加载排行榜，文件不存在则返回空列表"""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_to_leaderboard(nickname, level, score):
    """保存玩家记录到排行榜"""
    leaderboard = load_leaderboard()
    leaderboard.append({
        "nickname": nickname,
        "level": level,
        "score": score
    })
    # 按积分降序，积分相同按关卡降序
    leaderboard.sort(key=lambda x: (-x["score"], -x["level"]))
    # 只保留前 20 条记录
    leaderboard = leaderboard[:20]
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)


def show_leaderboard():
    """显示排行榜 TOP5"""
    leaderboard = load_leaderboard()
    print()
    print("========== 排行榜 TOP 5 ==========")
    if not leaderboard:
        print("  暂无记录，快来挑战吧！")
    else:
        print(f"  {'排名':<6}{'昵称':<12}{'关卡':<8}{'积分':<8}")
        print("  " + "-" * 34)
        for i, record in enumerate(leaderboard[:5], 1):
            print(f"  {i:<6}{record['nickname']:<12}{record['level']:<8}{record['score']:<8}")
    print("==================================")


# ==================== 游戏核心函数 ====================

def input_nickname():
    """输入玩家昵称"""
    while True:
        nickname = input("请输入你的昵称: ").strip()
        if nickname:
            return nickname
        print("昵称不能为空，请重新输入。")


def generate_question(level):
    """根据关卡等级生成题目，返回一道题目字典"""
    if level <= 5:
        # 关卡 1-5：100% 简单题
        pool = EASY_QUESTIONS
    elif level <= 10:
        # 关卡 6-10：60% 中等 + 40% 简单
        pool = MEDIUM_QUESTIONS * 3 + EASY_QUESTIONS * 2
    else:
        # 关卡 11+：60% 困难 + 40% 中等
        pool = HARD_QUESTIONS * 3 + MEDIUM_QUESTIONS * 2
    return random.choice(pool)


def check_answer(question, user_answer):
    """校验玩家答案，返回是否正确"""
    return user_answer.upper() == question["answer"]


def game_loop(nickname):
    """游戏主循环，返回 (最终关卡, 最终积分)"""
    level = 1       # 当前关卡
    hp = 3          # 生命值
    score = 0       # 积分

    while hp > 0:
        show_status(level, hp, score)
        question = generate_question(level)

        # 显示题目
        print(question["question"])
        print()
        for opt in question["options"]:
            print(f"  {opt}")
        print()

        # 获取玩家输入
        while True:
            user_answer = input("请输入你的答案 (A/B/C/D): ").strip().upper()
            if user_answer in ("A", "B", "C", "D"):
                break
            print("无效输入，请输入 A、B、C 或 D。")

        # 判断答案
        if check_answer(question, user_answer):
            score += 10
            print(f"\n  回答正确！ +10 分")
        else:
            hp -= 1
            correct = question["answer"]
            print(f"\n  回答错误！正确答案是 {correct}。")
            print(f"  提示：{question['hint']}")
            if hp > 0:
                print(f"  剩余生命值: {hp}")

        level += 1

    return level - 1, score


def game_over(nickname, level, score):
    """游戏结束，显示结果并更新排行榜"""
    print()
    print("╔══════════════════════════════════════╗")
    print("║           游戏结束！                ║")
    print("╚══════════════════════════════════════╝")
    print(f"  玩家: {nickname}")
    print(f"  到达关卡: {level}")
    print(f"  总积分: {score}")
    print()

    # 保存到排行榜
    save_to_leaderboard(nickname, level, score)
    print("  你的成绩已记录到排行榜！")


def start_game():
    """开始游戏流程"""
    nickname = input_nickname()
    print(f"\n欢迎你，{nickname}！游戏开始！")
    print("初始生命值: 3，答对 +10 分，答错 -1 生命值。")
    level, score = game_loop(nickname)
    game_over(nickname, level, score)


# ==================== 主入口 ====================

def main():
    """主入口函数，运行游戏主菜单循环"""
    show_banner()
    while True:
        show_menu()
        choice = input("请选择 (0/1/2): ").strip()
        if choice == "1":
            start_game()
        elif choice == "2":
            show_leaderboard()
        elif choice == "0":
            print("\n感谢游玩，再见！\n")
            break
        else:
            print("\n无效选择，请重新输入。")


if __name__ == "__main__":
    main()
