import ipywidgets as widgets
from IPython.display import display, clear_output
import os

class ImageTagger:
    def __init__(self, folder, tag_list, format='png'):
        self.folder = folder
        self.format = format
        self._tag_list = tag_list
        self._image_paths = [f'{folder}/{img}' for img in os.listdir(self.folder)
                                if img.endswith(f'.{self.format}')]
        self._total = len(self._image_paths)
        self.create_tag_dict()
        self._current_img = 0

        self._has_menu = False

    def create_tag_dict(self):
        self._tag_dict = {os.path.basename(k):'' for k in self._image_paths}

# - Beheavior methods -
    def mark_option(self, btn):
        ''' Mark current option '''
        btn.button_style = "" if btn.selected else "warning"
        btn.selected = not btn.selected

    def prev_img(self, btn):
        self.update_dict()
        if self._current_img > 0:
            self._current_img -= 1
        self.render()

    def next_img(self, btn):
        self.update_dict()
        if self._current_img < len(self._image_paths) -1:
            self._current_img += 1
        self.render()

    def update_dict(self):
        tag_opt = self.tag_menu
        tags = []
        for opt in tag_opt.children:
            if opt.selected:
                tags.append(opt.description)
        img_path = self._image_paths[self._current_img]
        img_title = os.path.basename(img_path)
        self._tag_dict[img_title] = ' '.join(tags)

    def update_opt_botton(self):
        assert self._has_menu, 'Menu has not been created!'
        img_path = self._image_paths[self._current_img]
        img_title = os.path.basename(img_path)
        tags = self._tag_dict[img_title]
        for opt in self.tag_menu.children:
            opt.selected = False
            opt.button_style = ""
            if opt.description in tags:
                opt.selected = True
                opt.button_style = "warning"


# - Construction methods
    def make_opt_button(self, opt):
        ''' Creates a buttom to add the tag '''
        btn = widgets.Button(description=opt)
        btn.on_click(self.mark_option)
        btn.selected = False
        return btn

    def make_next_button(self):
        btn = widgets.Button(description='Next >',
                            layout=widgets.Layout())
        btn.on_click(self.next_img)
        return btn

    def make_prev_button(self):
        btn = widgets.Button(description='< Prev',
                            layout=widgets.Layout())
        btn.on_click(self.prev_img)
        return btn

    def get_image(self):
        ''' Return the currant selected image '''
        return  open(self._image_paths[self._current_img], 'rb').read()

    def make_img_widget(self):
        img = widgets.Image(value=self.get_image(),
                            layout=widgets.Layout(width='300px', height='200px'),
                            format=self.format)
        return img

    def create_menu(self):
        self.progression = widgets.Label('')

        self.tag_menu = widgets.VBox([self.make_opt_button(o)
                                      for o in self._tag_list])
        self.display = self.make_img_widget()
        main_menu = widgets.HBox([self.display, self.tag_menu])

        next_but = self.make_next_button()
        prev_but = self.make_prev_button()
        move_menu = widgets.HBox([prev_but, next_but])
        self._has_menu = True

        display(widgets.VBox([self.progression, main_menu, move_menu]))

    def render(self):
        if not self._has_menu:
            self.create_menu()

        title = self._image_paths[self._current_img]
        self.progression.value = f'{title}  -  {self._current_img}/{self._total}'
        self.display.value = self.get_image()
        self.update_opt_botton()

    def to_csv(self, csv_name):
        with open(csv_name, 'w') as f:
            for k,v in self._tag_dict.items():
                f.write(f'{k},{v}\n')

    def read_csv(self, csv_name):
        self.create_tag_dict()
        with open(csv_name, 'r') as f:
            for line in f:
                k, v = line.split(',')
                self._tag_dict[k] = v.replace('\n','')


