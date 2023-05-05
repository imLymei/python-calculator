import PIL.Image
import customtkinter as ctk
import buttons
import darkdetect
import settings

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color=(settings.WHITE, settings.BLACK))
        self._set_appearance_mode('dark' if is_dark else 'light')
        self.geometry(f'{settings.APP_SIZE[0]}x{settings.APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')
        self.iconbitmap('./src/empty.ico')
        self.change_title_bar(is_dark)

        self.rowconfigure(list(range(settings.MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(settings.MAIN_COLUMNS)), weight=1, uniform='a')

        self.result_string = ctk.StringVar(value='0')
        self.formula_string = ctk.StringVar(value='')

        self.create_widgets()

        self.mainloop()

    def change_title_bar(self, is_dark):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            color = settings.TITLE_BAR_HEX_COLORS['dark'] if is_dark else settings.TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, byref(c_int(color)), sizeof(c_int))
        except:
            pass

    def create_widgets(self):
        main_font = ctk.CTkFont(family=settings.FONT, size=settings.NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=settings.FONT, size=settings.OUTPUT_FONT_SIZE, weight='bold')

        OutputLabel(self, 0, 'se', main_font, self.formula_string)
        OutputLabel(self, 1, 'e', result_font, self.result_string)

        self.create_buttons(main_font, result_font)

    def create_buttons(self, main_font, result_font):
        buttons.Button(master=self, function=self.percent, text=settings.OPERATORS['percent']['text'], font=main_font,
                       col=settings.OPERATORS['percent']['col'], row=settings.OPERATORS['percent']['row'])

        buttons.Button(master=self, function=self.clear, text=settings.OPERATORS['clear']['text'], font=main_font,
                       col=settings.OPERATORS['clear']['col'], row=settings.OPERATORS['clear']['row'])

        invert_light_image = PIL.Image.open(settings.OPERATORS['invert']['image path']['dark'])
        invert_dark_image = PIL.Image.open(settings.OPERATORS['invert']['image path']['light'])
        invert_image = ctk.CTkImage(invert_light_image, invert_dark_image)

        buttons.ImageButton(master=self, function=self.invert, col=settings.OPERATORS['invert']['col'],
                            row=settings.OPERATORS['invert']['row'], image=invert_image)

    def clear(self):
        print('clear')

    def percent(self):
        print('percent')

    def invert(self):
        print('invert')


class OutputLabel(ctk.CTkLabel):
    def __init__(self, master, row, anchor, font, string_variable):
        super().__init__(master, text='123', font=font, textvariable=string_variable)

        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)


if __name__ == '__main__':
    Calculator(darkdetect.isDark())
