import json
import glob
import os

# --- 配置 ---
# 输入文件匹配模式 (匹配当前目录下所有 json)
INPUT_PATTERN = '*.json'
# 输出文件名
OUTPUT_FILE = 'hitokoto_bundle.json'

def process_files():
    merged_data = []
    
    # 获取所有匹配的文件列表
    files = glob.glob(INPUT_PATTERN)
    
    print(f"找到 {len(files)} 个 JSON 文件，开始处理...")

    for file_path in files:
        # 跳过输出文件本身，防止无限循环读取
        if file_path == OUTPUT_FILE or file_path.endswith('package.json'):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 确保数据是一个列表
                if isinstance(data, list):
                    count = 0
                    for item in data:
                        # 提取核心字段，丢弃 id, uuid, creator 等无用信息
                        simplified_item = {
                            "hitokoto": item.get("hitokoto"),
                            "from": item.get("from")
                        }
                        
                        # 只有当句子内容存在时才添加
                        if simplified_item["hitokoto"]:
                            merged_data.append(simplified_item)
                            count += 1
                    
                    print(f"  -> {file_path}: 提取了 {count} 条句子")
                else:
                    print(f"  -> {file_path}: 格式不正确 (不是列表)，跳过。")

        except Exception as e:
            print(f"  -> {file_path}: 处理出错: {e}")

    # --- 写入结果 ---
    # ensure_ascii=False 保证输出的是中文而不是 \uXXXX 转义符
    # separators=(',', ':') 去除空格和换行，极致压缩体积 (如果你想要可读性，改用 indent=2)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, separators=(',', ':'))

    print("-" * 30)
    print(f"处理完成！")
    print(f"共合并句子: {len(merged_data)} 条")
    print(f"输出文件: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    process_files()