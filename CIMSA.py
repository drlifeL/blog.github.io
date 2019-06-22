import time
import pickle  # 导入序列化模块，方便序列化对象

Dict = {}  # 存储数据使用的字典


# --------商品类-------------
class Product:
    # provider 供应商   manager 经办人
    def __init__(self, name, num, unit, price, mark, provider, manager):
        self.name = name
        self.num = num
        self.unit = unit
        self.price = price
        self.mark = mark
        self.provider = provider
        self.manager = manager
        self.time = None
        self.stock = num

    '''
    日志格式 时间 行为 商品编号、商品名、数量、单位、价格、供货商、经办人、备注
     
    '''

    def saleLog(self, id, flag):
        curTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        info = curTime + " 操作：" + "入库" + " ID：" + id + " 数量：" + str(
            self.num) + " 单位：" + self.unit + " 名称：" + self.name + " 价格：" + self.price + " 供应商：" + self.provider + " 经办人:" + self.manager + " 备注：" + self.mark  # 默认是新增信息

        if not flag:  # false
            info = curTime + " 操作：" + "出库" + " ID：" + id + " 数量：" + str(
                self.num) + " 单位：" + self.unit + " 名称：" + self.name + " 价格：" + self.price + " 经办人:" + self.manager + " 备注：" + self.mark

        with open("Loginfo.txt", "a") as file:
            file.writelines(info + '\n')
            file.flush()
            file.close()


# --------初始化-------------
# 返回一个字典到内存中
def init():
    with open("product.cnf", "rb") as file:
        try:
            obj = pickle.load(file)
            return obj
        except EOFError:  # 如果读取错误，返回空字典
            return {}


def initUI():
    print("=" * 20)
    print("    仓库管理系统")
    print("   1.添加商品")
    print("   2.销售商品")
    print("   3.查看库存")
    print("   4.操作日志")
    print("   5.退出")
    print("=" * 20)


# 持久化字典到本地
def saveDictToFile():
    with open("product.cnf", "wb") as file:
        pickle.dump(Dict, file)


# --------主函数-------------
def main():
    global Dict
    Dict = init()  # 初始化存储字典
    while True:
        initUI()
        try:  # 发生异常后将已经在内存中的数据持久化到本地
            command = int(input("请输入功能对应数字："))
            if command == 1:
                add()
            elif command == 2:
                sale()
            elif command == 3:
                showInfo()
            elif command == 4:
                showLog()
            elif command == 5:
                saveDictToFile()
                print("欢迎下次使用！")
                break
            else:
                print("指令错误，请重新输入！")
        except Exception:
            print("输入有误，请重新输入！")
            saveDictToFile()


# 添加商品
def add():
    while True:
        id = input("请输入商品编号：")
        if not id:
            break
        name = input("请输入商品名称：")
        num = int(input("请输入商品数量："))
        unit = input("请输入商品单位：")
        price = input("请输入商品价格：")
        provider = input("请输入商品供应商：")
        manager = input("请输入商品经办人：")
        marks = input("请输入商品备注：")

        obj = Dict.get(id)
        if obj == None:
            Dict[id] = Product(name, num, unit, price, marks, provider, manager)
        else:  # 如果添加同一种商品，即出现覆盖行为
            temp = Dict(id).num + num
            Dict[id] = Product(name, temp, unit, price, marks, provider, manager)
        Dict[id].saleLog(id, True)


# 售出商品
def sale():
    print("商品编号     商品名    剩余数量     单位    单价    备注")
    for i in Dict.keys():
        fnum = 2
        lnum = len(Dict[i].name)
        if lnum % 2 == 0:
            fnum += 1
        print(f"  {i:^4}  {Dict[i].name:^14}   {str(Dict[i].stock):>{fnum}}   {Dict[i].unit:^8}  {Dict[i].price:^4}    {Dict[i].mark:^4}")
    while True:
        index = input("请输入要操作的商品编号：")
        if not index:
            break
        obj = Dict.get(index)
        if obj == None:
            print("商品编号错误，请重新输入！")
        else:
            objNum = obj.stock
            delNum = int(input("请输入售出的数量："))
            if delNum > objNum:  # 如果售出的数量大于本身的库存，那么则售出失败
                print("没有那么多货！")
            else:
                obj.manager = input("请输入经办人：")
                obj.stock -= delNum
                obj.num = delNum
                obj.saleLog(index, False)


# 商品信息
def showInfo():
    print("商品编号     商品名    剩余数量     单位    备注")
    for i in Dict.items():
        fnum = 4
        lnum = len(i[1].name)
        if lnum % 2 == 0:
            fnum += 1
        print(f"  {i[0]:^4}       {i[1].name:^4}    {str(i[1].stock):>{fnum}}        {i[1].unit:^4}   {i[1].mark:^4}")
    input("按任意键继续....")


# 操作日志
def showLog():
    with open("LogInfo.txt", "r") as file:
        print(file.read(), end="")
        file.close()
    input("按任意键退出....")


main()
