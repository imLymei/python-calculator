import customtkinter as ctk
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
        self.title('')
        self.iconbitmap('./src/empty.ico')

        self.change_title_bar(is_dark)

        self.mainloop()

    def change_title_bar(self, is_dark):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            COLOR = settings.TITLE_BAR_HEX_COLORS['dark'] if is_dark else settings.TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass


if __name__ == '__main__':
    Calculator(darkdetect.isDark())
