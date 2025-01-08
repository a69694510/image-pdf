from PIL import Image
import os
import re
from concurrent.futures import ThreadPoolExecutor

def natural_sort_key(file_name):
    """
    提取文件名中的数字部分，按自然顺序排序。
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', file_name)]

def create_pdf_from_images(folder_path):
    """
    将指定文件夹中的图片转换为 PDF，PDF 保存到上一级目录。
    """
    folder_name = os.path.basename(folder_path.rstrip(r"\/"))
    parent_folder = os.path.dirname(folder_path)  # 上一级目录路径
    output_pdf_path = os.path.join(parent_folder, f'{folder_name}.pdf')  # PDF 保存在上一级目录

    # 获取文件夹中所有图片文件并按自然顺序排序
    image_files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))],
        key=lambda x: natural_sort_key(os.path.basename(x))  # 按自然顺序排序
    )

    # 检查是否有图片
    if not image_files:
        print(f"目录 {folder_path} 中未找到任何图片文件，跳过...")
        return

    # 预加载图片
    image_list = []
    for img_path in image_files:
        img = Image.open(img_path)
        if img.mode != 'RGB':  # 转换为RGB模式，避免错误
            img = img.convert('RGB')
        image_list.append(img)

    # 保存为 PDF
    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:], quality=95, optimize=True)
    print(f'PDF 已成功生成，路径为: {output_pdf_path}')

def process_directory(folder_path):
    """
    处理单个目录，将图片转换为 PDF。
    """
    print(f"\n正在处理目录: {folder_path}")
    create_pdf_from_images(folder_path)

def process_all_directories(base_path, max_workers=4):
    """
    遍历当前目录中的所有子目录，并对每个子目录执行图片转换操作（支持多线程）。
    """
    directories_to_process = []

    # 找到所有包含图片的目录
    for root, dirs, files in os.walk(base_path):
        if any(file.lower().endswith(('jpg', 'jpeg', 'png')) for file in files):
            directories_to_process.append(root)

    # 并行处理每个目录
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_directory, directories_to_process)

if __name__ == "__main__":
    # 获取当前目录
    current_directory = os.getcwd()
    print(f"当前目录: {current_directory}")

    # 并行处理所有子目录
    process_all_directories(current_directory, max_workers=4)
