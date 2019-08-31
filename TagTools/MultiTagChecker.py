import ipywidgets as widgets
from IPython.display import display, clear_output

class MultiTagChecker:

    def __init__(self, model, data_set):
        self.model = model
        self.data_set = data_set
        self._total = len(data_set)
        self._tag_list = model.data.classes

        self._current_img = 0

        self._has_menu = False

    def set_DataSet(data_set):
        # Changer the data_set
        self.data_set = data_set

    # - Behavior methdos -
    def get_image(self):
        return self.data_set[self._current_img][0]._repr_png_()

    def prev_img(self, btn):
        if self._current_img > 0:
            self._current_img -= 1
        self.render()

    def next_img(self, btn):
        if self._current_img < self._total -1:
            self._current_img += 1
        self.render()

    def get_prediction(self):
        # Get the prediccted tags
        active_data = self.data_set[self._current_img][0]
        prediction = self.model.predict(active_data)
        if prediction:
            return prediction[0].obj

    def get_real(self):
        # Get the real tags
        return self.data_set[self._current_img][1].obj


    def update_opt_button(self):
        assert self._has_menu, 'Menu has not been created!'
        predicted_tags = self.get_prediction()
        real_tags = self.get_real()
        for opt in self.tag_menu.children:

            opt.button_style = ""
            if opt.description in real_tags:
                opt.button_style = "info"
                if opt.description in predicted_tags:
                    opt.button_style = "success"
            else:
                if opt.description in predicted_tags:
                    opt.button_style = "danger"

    # - Construct Methods -
    def make_opt_button(self, opt):
        ''' Creates a buttom to add the tag '''
        btn = widgets.Button(description=opt)
        btn.disabled = True
        btn.selected = False
        return btn

    def make_img_widget(self):
        img = widgets.Image(value=self.get_image(),
                          layout=widgets.Layout(width='300px', height='200px'))
        return img

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

        title = self.data_set.items[self._current_img]
        self.progression.value = \
            f'{title}  -  {self._current_img}/{self._total}'
        self.display.value = self.get_image()
        self.update_opt_button()
