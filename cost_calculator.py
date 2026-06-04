#!/usr/bin/env python3
"""
工装投标成本核算系统
使用方法：
    python cost_calculator.py <投标清单文件>

投标清单文件格式（CSV或简单文本）：
    序号,项目名称,单位,工程量,备注
    
    或
    
    1. 拆除砖墙 200m²
    2. 地砖铺贴_800×800 500m²
    3. 强电布线_暗敷_2.5mm² 800m
    ...
"""

import sys
import re
import csv
from pathlib import Path

# 成本数据库（内嵌，避免依赖外部文件）
COST_DB = {
    # 装修工程
    "拆除砖墙": {"unit": "m²", "labor": 45, "material": 5, "machine": 2, "mgmt": 0.06},
    "拆除地砖": {"unit": "m²", "labor": 30, "material": 3, "machine": 2, "mgmt": 0.06},
    "拆除吊顶": {"unit": "m²", "labor": 18, "material": 2, "machine": 1, "mgmt": 0.06},
    "砌轻质砖墙": {"unit": "m²", "labor": 55, "material": 60, "machine": 3, "mgmt": 0.06},
    "砌红砖墙": {"unit": "m²", "labor": 75, "material": 90, "machine": 3, "mgmt": 0.06},
    "墙面抹灰": {"unit": "m²", "labor": 28, "material": 18, "machine": 2, "mgmt": 0.06},
    "地面找平": {"unit": "m²", "labor": 20, "material": 10, "machine": 2, "mgmt": 0.06},
    "地砖铺贴_800×800": {"unit": "m²", "labor": 45, "material": 55, "machine": 3, "mgmt": 0.06},
    "地砖铺贴": {"unit": "m²", "labor": 45, "material": 55, "machine": 3, "mgmt": 0.06},
    "墙砖铺贴_300×600": {"unit": "m²", "labor": 40, "material": 48, "machine": 3, "mgmt": 0.06},
    "墙砖铺贴": {"unit": "m²", "labor": 40, "material": 48, "machine": 3, "mgmt": 0.06},
    "乳胶漆_一底两面": {"unit": "m²", "labor": 22, "material": 25, "machine": 2, "mgmt": 0.06},
    "乳胶漆": {"unit": "m²", "labor": 22, "material": 25, "machine": 2, "mgmt": 0.06},
    "墙纸铺贴": {"unit": "m²", "labor": 28, "material": 35, "machine": 2, "mgmt": 0.06},
    "石膏板平顶": {"unit": "m²", "labor": 50, "material": 65, "machine": 5, "mgmt": 0.06},
    "石膏板造型顶": {"unit": "m²", "labor": 75, "material": 95, "machine": 8, "mgmt": 0.06},
    "铝扣板吊顶": {"unit": "m²", "labor": 35, "material": 80, "machine": 3, "mgmt": 0.06},
    "矿棉板吊顶": {"unit": "m²", "labor": 30, "material": 50, "machine": 3, "mgmt": 0.06},
    "木饰面安装": {"unit": "m²", "labor": 65, "material": 120, "machine": 5, "mgmt": 0.06},
    "大理石墙面干挂": {"unit": "m²", "labor": 180, "material": 380, "machine": 15, "mgmt": 0.08},
    "实木门安装": {"unit": "樘", "labor": 350, "material": 1800, "machine": 20, "mgmt": 0.06},
    "铝合金推拉门": {"unit": "m²", "labor": 120, "material": 550, "machine": 10, "mgmt": 0.06},
    "断桥铝窗": {"unit": "m²", "labor": 110, "material": 700, "machine": 10, "mgmt": 0.06},
    "防水工程": {"unit": "m²", "labor": 30, "material": 40, "machine": 3, "mgmt": 0.06},
    "美缝": {"unit": "m", "labor": 10, "material": 5, "machine": 0, "mgmt": 0.06},
    "保洁": {"unit": "m²", "labor": 8, "material": 1, "machine": 0, "mgmt": 0.06},
    
    # 安装工程
    "强电布线_暗敷_2.5mm²": {"unit": "m", "labor": 18, "material": 12, "machine": 1, "mgmt": 0.06},
    "强电布线_暗敷_4mm²": {"unit": "m", "labor": 22, "material": 16, "machine": 1, "mgmt": 0.06},
    "强电布线_暗敷_6mm²": {"unit": "m", "labor": 28, "material": 22, "machine": 1, "mgmt": 0.06},
    "强电布线": {"unit": "m", "labor": 20, "material": 15, "machine": 1, "mgmt": 0.06},
    "弱电布线_网线": {"unit": "m", "labor": 12, "material": 8, "machine": 0, "mgmt": 0.06},
    "弱电布线_光纤": {"unit": "m", "labor": 15, "material": 12, "machine": 0, "mgmt": 0.06},
    "弱电布线": {"unit": "m", "labor": 12, "material": 8, "machine": 0, "mgmt": 0.06},
    "PPR给水管_Φ20": {"unit": "m", "labor": 22, "material": 15, "machine": 1, "mgmt": 0.06},
    "PPR给水管_Φ25": {"unit": "m", "labor": 26, "material": 20, "machine": 1, "mgmt": 0.06},
    "PPR给水管_Φ32": {"unit": "m", "labor": 32, "material": 28, "machine": 1, "mgmt": 0.06},
    "PPR给水管": {"unit": "m", "labor": 25, "material": 20, "machine": 1, "mgmt": 0.06},
    "给水管": {"unit": "m", "labor": 25, "material": 20, "machine": 1, "mgmt": 0.06},
    "排水管_PVC_Φ50": {"unit": "m", "labor": 18, "material": 15, "machine": 0, "mgmt": 0.06},
    "排水管_PVC_Φ75": {"unit": "m", "labor": 22, "material": 20, "machine": 0, "mgmt": 0.06},
    "排水管_PVC_Φ110": {"unit": "m", "labor": 28, "material": 28, "machine": 0, "mgmt": 0.06},
    "排水管": {"unit": "m", "labor": 22, "material": 20, "machine": 0, "mgmt": 0.06},
    "洁具安装_三件套": {"unit": "套", "labor": 500, "material": 800, "machine": 20, "mgmt": 0.06},
    "洁具安装": {"unit": "套", "labor": 500, "material": 800, "machine": 20, "mgmt": 0.06},
    "配电箱安装": {"unit": "台", "labor": 180, "material": 450, "machine": 15, "mgmt": 0.06},
    "桥架安装_100×50": {"unit": "m", "labor": 25, "material": 45, "machine": 3, "mgmt": 0.06},
    "桥架安装_200×100": {"unit": "m", "labor": 35, "material": 75, "machine": 5, "mgmt": 0.06},
    "桥架安装": {"unit": "m", "labor": 30, "material": 60, "machine": 4, "mgmt": 0.06},
    
    # 空调工程
    "多联机室内机安装_1-3匹": {"unit": "台", "labor": 450, "material": 280, "machine": 50, "mgmt": 0.06},
    "多联机室内机安装_5匹以上": {"unit": "台", "labor": 650, "material": 420, "machine": 80, "mgmt": 0.06},
    "多联机室内机安装": {"unit": "台", "labor": 500, "material": 320, "machine": 60, "mgmt": 0.06},
    "多联机室外机安装": {"unit": "台", "labor": 1200, "material": 800, "machine": 150, "mgmt": 0.06},
    "风管机安装": {"unit": "台", "labor": 800, "material": 550, "machine": 100, "mgmt": 0.06},
    "风机盘管安装": {"unit": "台", "labor": 350, "material": 280, "machine": 30, "mgmt": 0.06},
    "铜管安装_含保温": {"unit": "m", "labor": 55, "material": 85, "machine": 5, "mgmt": 0.06},
    "铜管安装": {"unit": "m", "labor": 55, "material": 85, "machine": 5, "mgmt": 0.06},
    "冷凝水管安装": {"unit": "m", "labor": 22, "material": 18, "machine": 2, "mgmt": 0.06},
    "风管制作安装_镀锌": {"unit": "m²", "labor": 45, "material": 85, "machine": 8, "mgmt": 0.06},
    "风管制作安装": {"unit": "m²", "labor": 45, "material": 85, "machine": 8, "mgmt": 0.06},
    "风口安装": {"unit": "个", "labor": 65, "material": 120, "machine": 5, "mgmt": 0.06},
    "系统调试_多联机": {"unit": "系统", "labor": 800, "material": 200, "machine": 100, "mgmt": 0.06},
    "系统调试_中央空调": {"unit": "系统", "labor": 1500, "material": 400, "machine": 200, "mgmt": 0.06},
    "系统调试": {"unit": "系统", "labor": 1000, "material": 300, "machine": 150, "mgmt": 0.06},
    
    # 消防工程
    "镀锌钢管安装_DN100": {"unit": "m", "labor": 35, "material": 85, "machine": 8, "mgmt": 0.06},
    "镀锌钢管安装_DN80": {"unit": "m", "labor": 28, "material": 65, "machine": 6, "mgmt": 0.06},
    "镀锌钢管安装_DN65": {"unit": "m", "labor": 22, "material": 52, "machine": 5, "mgmt": 0.06},
    "镀锌钢管安装_DN50": {"unit": "m", "labor": 18, "material": 40, "machine": 4, "mgmt": 0.06},
    "镀锌钢管安装_DN40": {"unit": "m", "labor": 15, "material": 32, "machine": 3, "mgmt": 0.06},
    "镀锌钢管安装_DN25": {"unit": "m", "labor": 12, "material": 22, "machine": 2, "mgmt": 0.06},
    "镀锌钢管安装": {"unit": "m", "labor": 22, "material": 50, "machine": 5, "mgmt": 0.06},
    "喷淋头安装_含管件": {"unit": "个", "labor": 45, "material": 55, "machine": 5, "mgmt": 0.06},
    "喷淋头安装": {"unit": "个", "labor": 45, "material": 55, "machine": 5, "mgmt": 0.06},
    "消火栓箱安装": {"unit": "套", "labor": 280, "material": 650, "machine": 30, "mgmt": 0.06},
    "消防泵安装": {"unit": "台", "labor": 1200, "material": 3500, "machine": 200, "mgmt": 0.06},
    "烟感探测器安装": {"unit": "个", "labor": 55, "material": 85, "machine": 5, "mgmt": 0.06},
    "温感探测器安装": {"unit": "个", "labor": 55, "material": 85, "machine": 5, "mgmt": 0.06},
    "探测器安装": {"unit": "个", "labor": 55, "material": 85, "machine": 5, "mgmt": 0.06},
    "手报按钮安装": {"unit": "个", "labor": 35, "material": 65, "machine": 3, "mgmt": 0.06},
    "声光报警器安装": {"unit": "个", "labor": 45, "material": 95, "machine": 5, "mgmt": 0.06},
    "消防模块安装": {"unit": "个", "labor": 55, "material": 120, "machine": 5, "mgmt": 0.06},
    "消防广播安装": {"unit": "个", "labor": 45, "material": 110, "machine": 5, "mgmt": 0.06},
    "消防电话安装": {"unit": "个", "labor": 35, "material": 85, "machine": 3, "mgmt": 0.06},
    "消防线缆敷设_NH-RVS": {"unit": "m", "labor": 8, "material": 4.5, "machine": 0, "mgmt": 0.06},
    "消防线缆敷设_NH-BV": {"unit": "m", "labor": 6, "material": 3.8, "machine": 0, "mgmt": 0.06},
    "消防线缆敷设": {"unit": "m", "labor": 7, "material": 4, "machine": 0, "mgmt": 0.06},
    "系统调试_自动报警": {"unit": "系统", "labor": 2000, "material": 800, "machine": 300, "mgmt": 0.06},
    "系统调试_自动喷淋": {"unit": "系统", "labor": 2500, "material": 1000, "machine": 400, "mgmt": 0.06},
}

# 取费标准
FEE_RATES = {
    "管理费率_一般": 0.06,
    "管理费率_复杂": 0.08,
    "利润率_竞争": 0.08,
    "利润率_正常": 0.12,
    "利润率_独家": 0.15,
    "增值税率": 0.09,
    "规费率": 0.008,
    "风险系数": 1.03,
}


def find_item(name: str) -> tuple:
    """模糊匹配项目"""
    # 精确匹配
    if name in COST_DB:
        return name, COST_DB[name]
    
    # 模糊匹配
    name_clean = name.replace(" ", "").replace("_", "").replace("、", "").lower()
    for key, value in COST_DB.items():
        key_clean = key.replace("_", "").replace("、", "").lower()
        if name_clean in key_clean or key_clean in name_clean:
            return key, value
    
    return None, None


def parse_quantity(text: str) -> float:
    """解析工程量"""
    # 移除常见单位，提取数字
    text = text.strip()
    # 匹配数字（支持小数）
    match = re.search(r'(\d+\.?\d*)', text.replace(',', ''))
    if match:
        return float(match.group(1))
    return 0


def calculate_item(name: str, quantity: float, profit_rate: float = 0.12) -> dict:
    """计算单个项目成本"""
    matched_name, item = find_item(name)
    
    if not item:
        return {
            "name": name,
            "matched": None,
            "quantity": quantity,
            "error": "未找到匹配项目"
        }
    
    labor = item["labor"] * quantity
    material = item["material"] * quantity
    machine = item["machine"] * quantity
    direct = labor + material + machine
    mgmt = direct * item["mgmt"]
    profit = (direct + mgmt) * profit_rate
    subtotal = direct + mgmt + profit
    tax = subtotal * FEE_RATES["增值税率"]
    total = subtotal + tax
    
    return {
        "name": name,
        "matched": matched_name,
        "unit": item["unit"],
        "quantity": quantity,
        "labor_unit": item["labor"],
        "material_unit": item["material"],
        "machine_unit": item["machine"],
        "labor_total": labor,
        "material_total": material,
        "machine_total": machine,
        "direct_cost": direct,
        "mgmt_cost": mgmt,
        "profit": profit,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }


def parse_input_file(filepath: str) -> list:
    """解析输入文件"""
    items = []
    path = Path(filepath)
    
    if not path.exists():
        print(f"错误：文件不存在 {filepath}")
        return items
    
    text = path.read_text(encoding='utf-8')
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # 尝试CSV格式
        if ',' in line:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 3:
                name = parts[1]
                qty = parse_quantity(parts[2])
                items.append((name, qty))
                continue
        
        # 尝试自然语言格式："1. 拆除砖墙 200m²" 或 "拆除砖墙 200"
        # 移除序号
        line = re.sub(r'^\d+[\.、\)]\s*', '', line)
        
        # 尝试提取名称和数量
        # 模式：名称 + 数字 + 单位
        match = re.match(r'^(.+?)\s+(\d+\.?\d*)\s*[m²m³个套台樘米m只片kg件系统]*$', line)
        if match:
            name = match.group(1).strip()
            qty = float(match.group(2))
            items.append((name, qty))
        else:
            # 尝试其他格式
            parts = line.split()
            if len(parts) >= 2:
                # 最后一个是数字
                try:
                    qty = float(parts[-1])
                    name = ' '.join(parts[:-1])
                    items.append((name, qty))
                except ValueError:
                    # 中间有数字
                    for i, part in enumerate(parts):
                        try:
                            qty = float(part)
                            name = ' '.join(parts[:i])
                            items.append((name, qty))
                            break
                        except ValueError:
                            continue
    
    return items


def format_currency(amount: float) -> str:
    """格式化金额"""
    return f"{amount:,.2f}"


def print_report(results: list, profit_rate: float = 0.12):
    """打印成本核算报告"""
    print("=" * 100)
    print("                         工装投标成本核算报告")
    print("                         适用地区：江苏省")
    print("=" * 100)
    print()
    
    # 表头
    print(f"{'序号':<4} {'项目名称':<20} {'单位':<4} {'工程量':>8} {'劳务单价':>10} {'材料单价':>10} {'机械单价':>10} {'综合单价':>10} {'合价':>12}")
    print("-" * 100)
    
    total_labor = 0
    total_material = 0
    total_machine = 0
    total_direct = 0
    total_all = 0
    
    for i, result in enumerate(results, 1):
        if "error" in result:
            print(f"{i:<4} {result['name']:<20} {'⚠️ 未匹配'}")
            continue
        
        unit_price = result["labor_unit"] + result["material_unit"] + result["machine_unit"]
        
        print(f"{i:<4} {result['name'][:20]:<20} {result['unit']:<4} {result['quantity']:>8.2f} "
              f"{result['labor_unit']:>10.2f} {result['material_unit']:>10.2f} {result['machine_unit']:>10.2f} "
              f"{unit_price:>10.2f} {result['total']:>12.2f}")
        
        total_labor += result["labor_total"]
        total_material += result["material_total"]
        total_machine += result["machine_total"]
        total_direct += result["direct_cost"]
        total_all += result["total"]
    
    print("-" * 100)
    
    # 汇总
    mgmt = total_direct * FEE_RATES["管理费率_一般"]
    profit = (total_direct + mgmt) * profit_rate
    subtotal = total_direct + mgmt + profit
    tax = subtotal * FEE_RATES["增值税率"]
    grand_total = subtotal + tax
    risk_total = grand_total * FEE_RATES["风险系数"]
    
    print()
    print("=" * 60)
    print("                         成本汇总")
    print("=" * 60)
    print(f"  人工费合计：                    {format_currency(total_labor):>15} 元")
    print(f"  材料费合计：                    {format_currency(total_material):>15} 元")
    print(f"  机械费合计：                    {format_currency(total_machine):>15} 元")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  直接费小计：                    {format_currency(total_direct):>15} 元")
    print(f"  管理费（6%）：                  {format_currency(mgmt):>15} 元")
    print(f"  利润（{int(profit_rate*100)}%）：                    {format_currency(profit):>15} 元")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  税前造价：                      {format_currency(subtotal):>15} 元")
    print(f"  增值税（9%）：                  {format_currency(tax):>15} 元")
    print(f"  ─────────────────────────────────────────────────")
    print(f"  投标总价：                      {format_currency(grand_total):>15} 元")
    print(f"  含风险系数（3%）：              {format_currency(risk_total):>15} 元")
    print("=" * 60)
    print()
    print(f"  劳务占比：{total_labor/grand_total*100:.1f}%  材料占比：{total_material/grand_total*100:.1f}%  "
          f"机械占比：{total_machine/grand_total*100:.1f}%")
    print()


def export_csv(results: list, filepath: str, profit_rate: float = 0.12):
    """导出CSV文件"""
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '项目名称', '单位', '工程量', '劳务单价', '材料单价', '机械单价', 
                         '综合单价', '劳务合价', '材料合价', '机械合价', '管理费', '利润', '税金', '合价'])
        
        for i, result in enumerate(results, 1):
            if "error" in result:
                writer.writerow([i, result['name'], '', '', '', '', '', '', '', '', '', '', '', '', '未匹配'])
                continue
            
            unit_price = result["labor_unit"] + result["material_unit"] + result["machine_unit"]
            writer.writerow([
                i, result['name'], result['unit'], result['quantity'],
                result['labor_unit'], result['material_unit'], result['machine_unit'],
                unit_price, result['labor_total'], result['material_total'], result['machine_total'],
                result['mgmt_cost'], result['profit'], result['tax'], result['total']
            ])
    
    print(f"✓ 已导出到：{filepath}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例清单文件内容：")
        print("  拆除砖墙 200")
        print("  地砖铺贴 500")
        print("  强电布线_暗敷_2.5mm² 800")
        print("  乳胶漆 1200")
        print("  多联机室内机安装 10")
        print("  镀锌钢管安装_DN100 150")
        print("  喷淋头安装 80")
        sys.exit(1)
    
    filepath = sys.argv[1]
    profit_rate = float(sys.argv[2]) if len(sys.argv) > 2 else 0.12
    
    items = parse_input_file(filepath)
    
    if not items:
        print("未能从文件中解析出任何项目")
        sys.exit(1)
    
    results = []
    for name, qty in items:
        result = calculate_item(name, qty, profit_rate)
        results.append(result)
    
    print_report(results, profit_rate)
    
    # 导出CSV
    csv_path = filepath.rsplit('.', 1)[0] + '_成本核算.csv'
    export_csv(results, csv_path, profit_rate)


if __name__ == '__main__':
    main()
