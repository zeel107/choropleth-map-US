import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial


image_file_name = 'choropleth_map.png'
button_text = ['T10', 'T12', 'T13', 'T16', 'T19', 'T23', 'T24', 'T25']
title_text = ['Alcoholic Beverages Sales Tax', 'Insurance Premiums Sales Tax', 'Motor Fuels Sales Tax',
              'Tobacco Products Sales Tax', 'Other Selective Sales and Gross Receipts Taxes',
              'Hunting and Fishing License', 'Motor Vehicles License', 'Motor Vehicles Operators License']
views = ['T10', 'T12', 'T13', 'T16', 'T19', 'T23', 'T24', 'T25']
current_views = ['T10', 'T12']
current_titles = ['Alcoholic Beverages Sales Tax', 'Insurance Premiums Sales Tax']
# T10,T12,T13,T16,T19,T23,T24,T25
class App():

    def __init__(self):

        self.root = tk.Tk()
        w, h = self.root.winfo_screenwidth() - 100, self.root.winfo_screenheight() - 100
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.title("Choropleth map")

        self.button_list = []

        self.left_buttons = tk.Frame(self.root)
        self.left_buttons.pack(side=tk.LEFT, anchor=tk.N)
        self.right_buttons = tk.Frame(self.root)
        self.right_buttons.pack(side=tk.RIGHT, anchor=tk.N)

        for i in range(4):
            self.button_list.append(tk.Button(self.left_buttons, text=button_text[i], command=partial(self.change_vis, i)))
            self.button_list[i].pack(side=tk.LEFT, pady = 3, padx = 3)

        for i in range(4, 8):
            self.button_list.append(tk.Button(self.right_buttons, text=button_text[i], command=partial(self.change_vis, i)))
            self.button_list[i].pack(side=tk.LEFT, pady = 3, padx = 3)

        self.image_width = w - 200
        self.image_height = h - 100

        self.fig = make_subplots(rows=1, cols=2, subplot_titles=[current_titles[0], current_titles[1]],
                            specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])
        self.fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[0]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=0.46)), row=1, col=1)

        self.fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[1]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=1.02)), row=1, col=2)

        self.fig.update_geos(
            visible=False, resolution=110, scope="usa",
            showcountries=True, countrycolor="Black"
        )
        self.fig.update_layout(width=self.image_width,
                               height=self.image_height, margin={"r": 0, "t": 100, "l": 0, "b": 0})
        self.fig.write_image(image_file_name)

        self.map_image = Image.open(image_file_name)
        self.map_photo = ImageTk.PhotoImage(self.map_image)



        self.cv = tk.Canvas(width=self.image_width, height=self.image_height)
        self.cv.create_image(0, 0, image=self.map_photo, anchor='nw')
        self.cv.pack(anchor=tk.S)
        self.root.after(200, lambda:self.change_vis(0))  # run the change_vis function .2 seconds after the root window main loop begins
        self.root.mainloop()



    def change_vis(self, button_num):
        print(button_num)
        if (button_num > 3):  # only the right side of the figure should be changed
            current_views[1] = views[button_num]
            current_titles[1] = title_text[button_num]
        else:
            current_views[0] = views[button_num]
            current_titles[0] = title_text[button_num]

        self.fig = make_subplots(rows=1, cols=2, subplot_titles=[current_titles[0], current_titles[1]],
                            specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])
        self.fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[0]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=0.46)), row=1, col=1)

        self.fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[1]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=1.02)), row=1, col=2)

        self.fig.update_geos(
            visible=False, resolution=110, scope="usa",
            showcountries=True, countrycolor="Black"
        )
        self.image_width = self.root.winfo_width() - self.left_buttons.winfo_width() - self.right_buttons.winfo_width() - 10
        self.image_height = self.root.winfo_height() - 10
        self.fig.update_layout(width=self.image_width, height=self.image_height, margin={"r": 0, "t": 100, "l": 0, "b": 0})
        self.fig.write_image(image_file_name)
        self.map_image = Image.open(image_file_name)
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.cv.destroy()
        self.cv = tk.Canvas(width=self.image_width, height=self.image_height)
        self.cv.create_image(0, 0, image=self.map_photo, anchor='nw')
        self.cv.pack(anchor=tk.S)

GEOJSON_FILE = "USStates.geojson"
df = pd.read_csv("normalizedTaxData.csv")

myapp = App()
