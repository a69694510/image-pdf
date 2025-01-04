from PIL import Image
import os
import argparse
import re

def natural_sort_key(file_name):
    """
    提取文件名中的数字部分，按自然顺序排序。
    """
    # 使用正则表达式分割文件名中的数字部分
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', file_name)]

def create_pdf_from_images(folder_path):
    # 获取文件夹名字，作为输出 PDF 的名字
    folder_name = os.path.basename(folder_path.rstrip(r"\/"))
    output_pdf_path = os.path.join(os.path.dirname(folder_path), f'{folder_name}.pdf')

    # 获取文件夹中所有图片文件并按自然顺序排序
    image_files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))],
        key=lambda x: natural_sort_key(os.path.basename(x))  # 按自然顺序排序
    )

    # 检查是否有图片
    if not image_files:
        print("未在文件夹中找到任何图片文件，请检查路径或图片格式！")
        return

    # 打开图片并按顺序处理
    image_list = []
    for img_path in image_files:
        print(f"正在处理图片: {img_path}")  # 打印当前处理的图片，方便调试
        img = Image.open(img_path)
        if img.mode != 'RGB':  # 转换为RGB模式，避免错误
            img = img.convert('RGB')
        image_list.append(img)

    # 保存为PDF
    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
    print(f'PDF 已成功生成，路径为: {output_pdf_path}')

if __name__ == "__main__":
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="将文件夹中的图片按自然顺序转换为 PDF")
    parser.add_argument(
        "folder_path", type=str, help="包含图片的文件夹路径"
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用主函数
    create_pdf_from_images(args.folder_path)
