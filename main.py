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
        self.display_nums = []
        self.full_operation = []

        self.create_widgets(is_dark)

        self.mainloop()

    def change_title_bar(self, is_dark):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            color = settings.TITLE_BAR_HEX_COLORS['dark'] if is_dark else settings.TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, byref(c_int(color)), sizeof(c_int))
        except:
            pass

    def create_widgets(self, is_dark):
        main_font = ctk.CTkFont(family=settings.FONT, size=settings.NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=settings.FONT, size=settings.OUTPUT_FONT_SIZE, weight='bold')

        color = settings.BLACK if is_dark else settings.WHITE
        text_color = settings.WHITE if is_dark else settings.BLACK

        OutputLabel(self, 0, 'se', main_font, self.formula_string, color, text_color)
        OutputLabel(self, 1, 'e', result_font, self.result_string, color, text_color)

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

        for number, data in settings.NUM_POSITIONS.items():
            buttons.NumButton(master=self, text=number, function=self.number_pressed, col=data['col'],
                              row=data['row'], font=main_font, column_span=data['span'])

        for operator, data in settings.MATH_POSITIONS.items():
            if data['character']:
                buttons.MathButton(master=self, text=data['character'], function=self.math_pressed,
                                   operator=operator, col=data['col'], row=data['row'], font=main_font)
            else:
                light_image = PIL.Image.open(data['image path']['light'])
                dark_image = PIL.Image.open(data['image path']['dark'])
                divide_image = ctk.CTkImage(dark_image, light_image)
                buttons.MathImageButton(master=self, function=self.math_pressed, operator=operator, col=data['col'],
                                        row=data['row'],
                                        image=divide_image)

    def clear(self):
        self.display_nums.clear()
        self.result_string.set('0')

    def percent(self):
        if self.display_nums:
            full_number = float(''.join(self.display_nums))

            if full_number > 0:
                if full_number >= 1:
                    new_nums = full_number / 100
                    self.display_nums.clear()

                    new_nums = self.check_if_integer(new_nums)

                    for data in str(new_nums):
                        self.display_nums.append(data)
                else:
                    new_nums = full_number * 100
                    self.display_nums.clear()

                    new_nums = self.check_if_integer(new_nums)

                    for data in str(new_nums):
                        self.display_nums.append(data)
                self.result_string.set(new_nums)

    def invert(self):
        if self.display_nums:
            last_number = self.display_nums[0]
            self.display_nums[0] = f'-{last_number}' if last_number[0] != '-' else last_number[1:]

            full_number = ''.join(self.display_nums)
            self.result_string.set(full_number)

    def number_pressed(self, value):
        if (value == '.' and not self.display_nums.__contains__('.')) or value != '.':
            self.display_nums.append(str(value))
            full_number = ''.join(self.display_nums)
            self.result_string.set(full_number)

    def math_pressed(self, value):
        current_number = ''.join(self.display_nums)
        self.full_operation.append(current_number)

        if current_number:
            if value != '=':
                self.full_operation.append(value)
                self.display_nums.clear()

                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))
            else:
                result = eval(' '.join(self.full_operation))

                if isinstance(result, float):
                    result = self.check_if_integer(result)

                self.display_nums = [str(result)]
                self.result_string.set(result)
                self.full_operation.append(f'= {result}')
                self.formula_string.set(' '.join(self.full_operation))
                self.full_operation.clear()

    def check_if_integer(self, value):
        if value % 1 == 0:
            value = int(value)
        else:
            value = round(value, 3)
        return value


class OutputLabel(ctk.CTkLabel):
    def __init__(self, master, row, anchor, font, string_variable, color=settings.BLACK, text_color=settings.WHITE):
        super().__init__(master, text='123', font=font, textvariable=string_variable, fg_color=color,
                         text_color=text_color)

        self.grid(column=0, columnspan=4, row=row, sticky=anchor, padx=10)


if __name__ == '__main__':
    Calculator(darkdetect.isDark())
