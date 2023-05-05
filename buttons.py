from customtkinter import CTkButton
import settings

class Button(CTkButton):
    def __init__(self, master, text, function, col, row, font, color='dark-gray'):
        super().__init__(master, text=text, corner_radius=settings.STYLING['corner-radius'], command=function,
                         font=font, fg_color=settings.COLORS[color]['fg'], hover_color=settings.COLORS[color]['hover'],
                         text_color=settings.COLORS[color]['text'])

        self.grid(column=col, row=row, sticky='nswe', padx=1, pady=1)