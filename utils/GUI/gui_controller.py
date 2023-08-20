from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk
from imutils.video import VideoStream


# util functions
from utils import contour_generator as cg

# NOTICE : 如果Python没有使用 - O选项启动，__debug__是真值，否则是假值。
# 注意   : -O 是放在python后面，作为python的argument
# e.g.   : python -O .\gui_controller.py
RESIZE_CONST = 150


def event_handler(event, callback):
    event.widget.config(bg='light blue')
    event.widget.focus_set()  # give keyboard focus to the label
    # event.widget.bind('<Key>', edit)
    callback()


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        # 程序框体的名称
        self.title("Shooting Simulator")
        self.minsize(640, 400)

        # 用于容纳按钮
        self.file_browser_labelframe = ttk.LabelFrame(self, text="Open File")
        self.file_browser_labelframe.grid(column=0, row=1, padx=20, pady=20)

        # 用于容纳image property
        self.image_property_labelframe = ttk.LabelFrame(
            self, text="Image Property")
        self.image_property_labelframe.grid(column=2, row=5, padx=20, pady=20)

        # 确认
        self.button_image_selection()
        self.button_confirm()
        # self.button_generate_contour()

    # 判断图片的大小

    def read_target_size(self):
        '''
        Reads the height and width of the target image.
        Args:
        '''
        # 首先读取图片
        print('read_target_size')
        img = cv2.imread(self.filename)
        # 打印出 width 和 length
        height = img.shape[0]
        width = img.shape[1]
        print(height, width)
        return height, width

    # 判断图片的大小
    def display_target_size(self):
        '''
        Reads the height and width of the target image.
        Args:
        '''
        height, width = self.read_target_size()
        self.label_img_size = ttk.Label(
            self.image_property_labelframe, text="WTF")
        self.label_img_size.grid(column=2, row=4)
        self.label_img_size.configure(text=f"width:{width} height: {height} ")

    # 按下按钮确认图片后:
    def button_confirm(self):
        # NOTICE: 带参数的function要用lambda
        # 注意  ： 不带参数的，如果用了"lambda:"关键字，要加括号，否则不加括号
        self.button_confirm = ttk.Button(
            self.file_browser_labelframe, text="Confirm", command=lambda: self.display_target_size())
        self.button_confirm.grid(column=2, row=1)
        # TODO： 用state来处理这些
        # TODO： 显示下一步
        self.button_generate_contour()

    # 浏览图片
    def button_image_selection(self):
        self.button_image_selection = ttk.Button(
            self.file_browser_labelframe, text="Browse A Target", command=self.fileDialog)
        self.button_image_selection.grid(column=1, row=1)

    # 显示目标的缩略图
    def show_target_thumbnail(self, img):
        '''
        显示缩略图
        '''
        if (__debug__ == True):
            print("Showing Target Thumbnail Picture")

        print("img.size()")
        print(img.size)
        height = img.size[0]
        width = img.size[1]

        # TODO: 这样弄出来比例不太对
        img = img.resize(
            (round(RESIZE_CONST/height*width), round(RESIZE_CONST)))

        photo = ImageTk.PhotoImage(img)

        # 显示缩略图
        self.image_display_label = Label(image=photo)
        self.image_display_label.image = None
        self.image_display_label.image = photo
        self.image_display_label.grid(column=2, row=4)

        # 显示大图
        self.image_display_label.bind("<Button>", self.show_full_image)

    # 浏览文件的对话框
    def fileDialog(self):
        # 左上角的对话框名字
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select An Image", filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        self.label = ttk.Label(self.file_browser_labelframe, text="")

        #
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        print(self.filename)

        # 打开image
        img = Image.open(self.filename)
        self.show_target_thumbnail(img)

        # target_image 存到class里面
        self.target_image = img

    # 点击后会弹出cv2读取的大图

    def show_full_image(self, event):
        if __debug__:
            print(event)

        try:
            # 用 cv2 读取文件名，并且显示出来
            target_img = cv2.imread(self.filename)
            cv2.imshow("target_img", target_img)
        except Exception as e:
            print(e)
            pass

    # generate_contour
    def generate_contour(self):
        # class 当中存 contours
        self.generated_cnts, self.generated_dialation = cg.contour_generator(
            self.target_image)

        # generate contour 的按钮,按下后执行 generate_contour()

    def button_generate_contour(self):
        if(__debug__):
            print("Generating Contour")
        self.button_generate_contour = ttk.Button(
            self.file_browser_labelframe, text="Generate Target Contours", command=lambda: self.generate_contour())
        self.button_generate_contour.grid(column=0, row=4)

    class video_handler:
        """Inner class testing"""

        def __init__(self):
            self.run_stream()

        def run_stream(self):
            self.stream = VideoStream(
                usePiCamera=False, resolution=(320, 240)).start()


root = Root()
root.mainloop()
