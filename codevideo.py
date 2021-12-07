from PIL import Image,ImageFilter,ImageDraw, ImageFont
import os
import sys



# 创建临时文件夹
def creatTemp(temp):
    if not os.path.exists(temp):
        os.makedirs(temp)

# 加载文本
def load_file(file_name):
    contents = []
    with open(file_name,'r',encoding='utf-8') as f:
        contents = f.readlines()
    return contents

# 将文本画出来
def draw_content(contents,video_size,background,margin_top,margin_left,font_size,line_space):
    video_width,video_height = video_size
    max_lines = (video_height - margin_top * 2) / (font_size + line_space)
    image_name = 0
    start_row = 0 # 开始绘制的行 数组中
    current_line = 1 # 当前正在写的行
    start_column = 0 # 开始绘制的列
    font = ImageFont.truetype(font='consola.ttf',size=font_size-2)
    for current_row in range(0,len(contents)): #len(contents)
        img = Image.new('RGB', video_size, background) # 创建1920*1080的画布
        draw = ImageDraw.Draw(img)

        # 先绘制前面的行，从开始行绘制到结束行
        line_add = 0
        for i in range(start_row,current_row):
            y = margin_top + line_add * (font_size + line_space)
            draw.text(xy=(margin_left, y), text=contents[i],fill=(0, 255, 0), font=font)
            line_add += 1 #为下一行内容计算y坐标做准备，没有这个内容会重叠在一起

        # 再绘制当前行的字符
        y = margin_top + (current_line - 1) * font_size
        for current_column in range(0,len(contents[current_row])):
            draw.text(xy=(margin_left, y), text=contents[current_row][:current_column]+"|",fill=(0, 255, 0), font=font)
            img.save('temp/image'+str(image_name).zfill(4)+'.jpg')
            draw.rectangle((margin_left,y,video_width - margin_left,y + font_size),fill = background) # 消除刚写的一行，防止重叠
            image_name += 1

        if current_line < max_lines: # 屏幕没满
            current_line += 1 #往下写
        else:
            # 屏幕写满
            start_row += 1 #往上滚动

    # 返回图片的数量
    return image_name

# 将图片转换成视频
def create_video(temp,bgm):
    ffmpeg_command = 'ffmpeg -f image2 -i '+os.path.join(temp,'image%04d.jpg')+' -i '+bgm+' -vcodec libx264 -r 10  codeshow.mp4'
    os.system(ffmpeg_command)

def main():
    # 创建一个画布 1920*1080
    video_size = video_width,video_height = 1920, 1080
    margin_top = 90   # 上边距
    margin_left = 100 # 左边距
    font_size = 30    # 字体大小
    line_space = 0    #行间距
    
    temp = os.path.join(os.getcwd(),'temp') # 临时文件夹
    background = 0, 0, 0 # 背景色
    if len(sys.argv) < 3:
           print('Usage: python {name} [codefile] [bgm] [options:1920x1080(vide_size)]'.format(name = sys.argv[0]))
           exit(1)
    codefile=sys.argv[1]
    bgm=sys.argv[2]

    if len(sys.argv) > 3:
            video_width,video_height = sys.argv[4].split('x')
            video_size=int(video_width),int(video_height)
    creatTemp(temp)
    contents = load_file(codefile)
    image_total = draw_content(contents,video_size,background,margin_top,margin_left,font_size,line_space)
    create_video(temp,bgm)

if __name__ == '__main__':
    main()

