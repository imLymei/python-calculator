from customtkinter import CTkButton
import settings


class Button(CTkButton):
    def __init__(self, master, text, function, col, row, font, column_span=1, color='dark-gray'):
        super().__init__(master, text=text, corner_radius=settings.STYLING['corner-radius'], command=function,
                         font=font, fg_color=settings.COLORS[color]['fg'], hover_color=settings.COLORS[color]['hover'],
                         text_color=settings.COLORS[color]['text'])

        self.grid(column=col, columnspan=column_span, row=row, sticky='nswe', padx=settings.STYLING['gap'],
                  pady=settings.STYLING['gap'])


class NumButton(Button):
    def __init__(self, master, text, function, col, row, font, column_span):
        super().__init__(master=master, text=text, function=lambda: function(text), col=col, row=row, font=font, color='light-gray',
                         column_span=column_span)


class ImageButton(CTkButton):
    def __init__(self, master, function, col, row, image, text='', color='dark-gray'):
        super().__init__(master, text=text, corner_radius=settings.STYLING['corner-radius'], command=function,
                         fg_color=settings.COLORS[color]['fg'], hover_color=settings.COLORS[color]['hover'],
                         text_color=settings.COLORS[color]['text'], image=image)

        self.grid(column=col, row=row, sticky='nswe', padx=settings.STYLING['gap'], pady=settings.STYLING['gap'])
