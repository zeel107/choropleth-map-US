import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tkinter as tk
from PIL import Image, ImageTk
from functools import partial

image_width = 1200
image_height = 600
window_geometry = '1400x600'
image_file_name = 'chloroplath_map.png'
button_text = ['T01', 'T09', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15']
views = ['T01', 'T09', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15']
current_views = ['T01', 'T12']

class App():

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Chloroplath map")
        self.root.geometry(window_geometry)
        self.map_image = Image.open(image_file_name)
        self.map_photo = ImageTk.PhotoImage(self.map_image)

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

        self.cv = tk.Canvas(width=image_width, height=image_height)
        self.cv.create_image(0, 0, image=self.map_photo, anchor='nw')
        self.cv.pack(anchor=tk.S)
        self.root.mainloop()

    def change_vis(self, button_num):
        print(button_num)
        if (button_num > 3):  # only the right side of the figure should be changed
            current_views[1] = views[button_num]
        else:
            current_views[0] = views[button_num]

        fig = make_subplots(rows=1, cols=2, subplot_titles=[current_views[0], current_views[1]],
                            specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])
        fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[0]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=0.46)), row=1, col=1)

        fig.add_trace(
            go.Choropleth(locations=df['item'], z=df[current_views[1]], locationmode='USA-states',
                          colorbar=dict(thickness=20, x=1.02)), row=1, col=2)

        fig.update_geos(
            visible=False, resolution=110, scope="usa",
            showcountries=True, countrycolor="Black"
        )
        image_width = self.root.winfo_width() - self.left_buttons.winfo_width() - self.right_buttons.winfo_width() - 10
        image_height = self.root.winfo_height() - 10
        fig.update_layout(width=image_width, height=image_height, margin={"r": 0, "t": 100, "l": 0, "b": 0})
        fig.write_image(image_file_name)
        self.map_image = Image.open(image_file_name)
        self.map_photo = ImageTk.PhotoImage(self.map_image)
        self.cv.destroy()
        self.cv = tk.Canvas(width=image_width, height=image_height)
        self.cv.create_image(0, 0, image=self.map_photo, anchor='nw')
        self.cv.pack(anchor=tk.S)

GEOJSON_FILE = "USStates.geojson"
df = pd.read_csv("taxData2021.csv")

fig = make_subplots(rows=1, cols=2,subplot_titles=[current_views[0],current_views[1]],
                    specs=[[{'type':'choropleth'},{'type':'choropleth'}]])
fig.add_trace(
    go.Choropleth(locations=df['item'], z=df[current_views[0]], locationmode='USA-states', colorbar=dict(thickness=20, x=0.46) ), row=1, col=1)

fig.add_trace(
    go.Choropleth(locations=df['item'], z=df[current_views[1]], locationmode='USA-states', colorbar=dict(thickness=20, x=1.02)), row=1, col=2)

fig.update_geos(
    visible=False, resolution=110, scope="usa",
    showcountries=True, countrycolor="Black"
)
fig.update_layout(width=image_width, height=image_height, margin={"r":0,"t":100,"l":0,"b":0})
fig.write_image(image_file_name)

myapp = App()
