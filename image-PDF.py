from PIL import Image
import os

# 设置图片所在的文件夹路径
folder_path = r'H:\大众软件_1995-2016_img\1995年大众软件\POP199508'  # 替换为你的图片文件夹路径

# 获取文件夹名字，作为输出 PDF 的名字
folder_name = os.path.basename(folder_path.rstrip(r"\/"))  # 获取文件夹名称
output_pdf_path = os.path.join(os.path.dirname(folder_path), f'{folder_name}.pdf')  # 输出 PDF 路径

# 获取文件夹中所有图片文件
image_files = sorted(
    [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
)

# 检查是否有图片
if not image_files:
    print("未在文件夹中找到任何图片文件，请检查路径或图片格式！")
else:
    # 打开图片并转换为PDF
    image_list = []
    for img_path in image_files:
        img = Image.open(img_path)
        if img.mode != 'RGB':  # 转换为RGB模式，避免错误
            img = img.convert('RGB')
        image_list.append(img)

    # 保存为PDF
    image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
    print(f'PDF 已成功生成，路径为: {output_pdf_path}')
