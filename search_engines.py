import sqlite3
import csv
import json
import os

# 修改为你自己的 Web Data 路径
WEB_DATA_PATH = os.path.expanduser(
    r"D:\Chrome\Chrome\Data\Default\Web Data"
)

# 输出文件名
CSV_FILE = "search_engines.csv"
JSON_FILE = "search_engines.json"

def export_search_engines_sorted(db_path):
    if not os.path.exists(db_path):
        print("❌ 错误：找不到 Web Data 文件，请确认路径是否正确。")
        return

    # 连接 SQLite 数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询 keywords 表，按 keyword 字母顺序排序（不区分大小写）
    cursor.execute("SELECT short_name, keyword, url FROM keywords ORDER BY keyword COLLATE NOCASE")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ 没有找到任何搜索引擎配置。")
        return

    # 写入 CSV 文件
    with open(CSV_FILE, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "keyword", "url"])
        writer.writerows(rows)

    # 写入 JSON 文件
    engines_list = [{"name": name, "keyword": keyword, "url": url} for name, keyword, url in rows]
    with open(JSON_FILE, "w", encoding="utf-8") as jsonfile:
        json.dump(engines_list, jsonfile, indent=4, ensure_ascii=False)

    print(f"✅ 导出完成！已保存为：\n  - {CSV_FILE}\n  - {JSON_FILE}")

    conn.close()

if __name__ == "__main__":
    export_search_engines_sorted(WEB_DATA_PATH)

#首先关闭所有 Chrome 浏览器窗口
#命令python search_engines.py