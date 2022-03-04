'''
    本模块主要实现xlwt 导出到excel样式
'''
import xlwt
class xlsStyleSet():
    def __init__(self,
                 align_horz,
                 align_vert,
                 borders_l = 1,
                 borders_r = 1,
                 borders_t = 1,
                 borders_b =1 ,
                 font_name = '宋体',
                 font_bold = False,
                 font_underline = False,
                 font_italic = False,
                 font_height = 20*18,
                 align_wrap = 1
                 ):

        '''
        :param font_name: 字体类型，eg:宋体
        :param font_bold: 字体加粗，默认false
        :param font_height: 字体大小（20*x  20是基数不变，x是字号用于调整大小）
        :param font_underline:字体下划线（True,False）
        :param font_italic:字体斜体字（True,False）
        :param align_horz:单元格水平对齐  【0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)】
        :param align_vert:单元格垂直对齐  【0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)】
        :param align_wrap:自动换行【1】
        # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
        :param borders_l:单元格边框（左）
        :param borders_r:单元格边框（右）
        :param borders_t:单元格边框（上）
        :param borders_b:单元格边框（下）
        '''
        # 初始化样式
        self.style = xlwt.XFStyle()
        self.font_name = font_name
        self.font_height = font_height
        self.font_bold = font_bold
        self.font_underline = font_underline
        self.font_italic = font_italic
        self.align_horz = align_horz
        self.align_vert = align_vert
        self.align_wrap = align_wrap
        self.borders_l = borders_l
        self.borders_r = borders_r
        self.borders_t = borders_t
        self.borders_b = borders_b


    # 设置边框样式
    def setBorders(self):
        borders = xlwt.Borders()
        # borders.left = xlwt.Borders.THIN
        # borders.right = xlwt.Borders.THIN
        # borders.top = xlwt.Borders.THIN
        # borders.bottom = xlwt.Borders.THIN
        borders.left = self.borders_l
        borders.right = self.borders_r
        borders.top = self.borders_t
        borders.bottom = self.borders_b
        return borders

    # 设置字体
    def setFont(self):
        font = xlwt.Font()
        font.bold = self.font_bold
        font.height = self.font_height
        font.name = self.font_name
        return font

    # 设置对齐方式
    def setAlign(self):
        align = xlwt.Alignment()
        align.horz = self.align_horz
        align.vert = self.align_vert
        return align

    # 针对表头设置全局样式
    def getStyle(self):
        style = xlwt.XFStyle()
        style.font = self.setFont()
        style.borders = self.setBorders()
        style.alignment = self.setAlign()
        return style