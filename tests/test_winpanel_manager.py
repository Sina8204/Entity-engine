from ursina import *
from typing import Union, Tuple
            
class PanelManager:
    def __init__(self , **shared_values):
        self.shared_values = shared_values
        self.panels = {}
    
    def add_panels(self , **panels : WindowPanel):
        """
        The input arguments should be as follows : panel_name = WindowPanel(title = str , content(UI_class1 , UI_class2 , ...) , enabled = False)
        - Tip :
                Arguments WindowPanel 'enabeled' value must be 'False'
        + For exampel ) A panel manager with 'name' , 'age' & 'city' panels :
                panel_manager = PanelManager()
                panel_manager.add_panels(
                                        name = WindowPanel(title="Panel name" , content = (
                                                            Text(name = "name_text" , text = "panel name") , 
                                                            Button( name = 'panel_age' , text = 'Go to age panel') , 
                                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                                            ) , enabled = False
                                                        ) ,
                                        age = WindowPanel(title= "Panel age" , content = (
                                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                                            Text(name = "age_text" , text = "panel age"),
                                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                                            ) , enabled = False
                                                        ) ,
                                        city = WindowPanel(title= "Panel city" , content = (
                                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                                            Button( name = 'panel_age' , text = 'Go to age panel') ,
                                                            Text(name = "city_text" , text ="panel city")
                                                            ) , enabled = False
                                                        )
                                        )
                panel_manager.enabel_panel('name') # At first , active and show panel 'name'
        """
        for key , value in list(panels.items()):
            if not isinstance(value , WindowPanel):
                raise ValueError(f"Argument value type shuld be 'WindowPanel'. But you enterd {key} = {value} and {value} type is {type(value)}")
            self.panels.update({key : value})
    
    def connect_panel_buttons(self , **ButtonName_TargetPanel):
        """
        Panels have buttons to navigate to other panels
        So you can use this method to connect buttons to their panel.
        Just pass arguments to this method like this : Button_name = 'panel_name'

        - Tip : 
                panel_name is the argument name that you creat WindowPanel by method add_panels.

        * Attention : 
                The name of a button attached to a panel , must be the same in all panels.
                Otherwise , you will encounter a logic error.
        + For exampel:
                panel_manager.connect_panel_buttons(panel_name = 'name' , panel_age = 'age' , panel_city = 'city')
        """
        for current_panel in list(self.panels.keys()):
            for btn_name , target_panel in list(ButtonName_TargetPanel.items()):
                if self._isthere(current_panel , Button , btn_name):
                    btn_index = self._get_widget_index(name = btn_name , panel_name=current_panel , widget_type=Button)
                    if btn_index != None : 
                        self.button_connection(current_panel , target_panel , btn_index)
                        print(f"{current_panel} : {btn_name}({btn_index}) --> {target_panel}")
    
    def enabel_panel(self , panel_name : str):
        """
        By use this method , you can show a panel. Just input panel_name as 'str'
        """
        self.hide_panels()
        self.panels[panel_name].enabled = True
    
    def set_position(self , x = 0.0 , y = 0.0 , mode = "custom"):
        """
        You shuld use this method for set position of the panel.
        By 'mode' argument you can set position at center:
                    mode = 'y_center' : sets the panel position on the vertical axis to the center.
                    mode = 'x_center' : sets the panel position on the horizontal axis to the center.
        + example :
            1) 'custom'   : panel_manager.set_position(x = 0.55 , y = 0.45)
            2) 'y_center' : panel_manager.set_position(x = 0.6 , mode='y_center')
            3) 'x_center' : panel_manager.set_position(y = 0.5 , mode='x_center')
        """
        match (mode):
            case "custom": 
                for key , value in list(self.panels.items()):
                    self.panels[key].position = (x , y)
                    self.panels[key].layout()
            case "y_center":
                for key , value in list(self.panels.items()):
                    self.panels[key].y = self.panels[key].panel.scale_y / 2 * self.panels[key].scale_y
                    self.panels[key].x = x
                    self.panels[key].layout()
            case "x_center":
                for key , value in list(self.panels.items()):
                    self.panels[key].position = (0 , y)
                    self.panels[key].layout()
    
    def set_content_attr(self , panel_name = '' , index_of_content = None , content = None , attr = '' , value = None):
        """
        You shuld use 'set_content_attr' method when you want change 
        value of a panel widget attribute like '.text' , '.name' , 'position' and etc.
        - guid :
                1) At first select widget panel name by argument 'panel_name' as str.
                2) you can use one of the arguments 'index_of_content' and 'content' for choose your widget :
                        - index_of_content : when you want choose your widget by its index at the tuple of WindowPanel content. 
                        - content : when you want choose your widget by its 'name' and 'ui class'.
                    * Attention : 
                                content type mest be a tuple with two index like '('widget_name' , widget_class)'.
                                if index_of_content and content , content becomes None and index_of_content is considered.
                3) Choose your attribute by argument 'attr' as a str.
                4) input your value by argument 'value'
        
        + example :
                    # Choose content by index_of_content :
                        panel_manager.set_content_attr(
                                                        panel_name = 'age' , 
                                                        index_of_content = 1 , 
                                                        attr='text' , 
                                                        value="Here is age panel"
                                                    )
                    # Choose content by its name and ui class :
                        panel_manager.set_content_attr(
                                                        panel_name = 'city' , 
                                                        content=('city_text' , Text) , 
                                                        attr='text' , 
                                                        value="Here is panel city"
                                                    )
        """
        error = "One of the arguments index_of_content and content must have value!!"
        help1 = "content must be a tuple like ('content_name' , content_class)"
        help2 = "index_of_content must be integer"
        help3 = "if index_of_content and content , content becomes None and index_of_content is considered"

        if index_of_content is not None and content is not None:
            content = None
        if index_of_content is None and content is None:
            raise ValueError(f"{error} Use this guid :\n\t1){help1}\n\t2){help2} \n\t3){help3}")
        if index_of_content is None and not isinstance(content , tuple):
            raise ValueError(f"{help1}. But you enterd {content} that type is {type(content)}")
        if not isinstance(index_of_content , int) and content is None:
            raise ValueError(f"{help2}. But you enterd {content} that type is {type(content)}")
        if isinstance(content , tuple):
            if len(content) > 2 or len(content) < 2:
                raise ValueError(f"content must have 2 index like ('content_name' , content_class)")
            if not isinstance(content[0] , str):
                raise ValueError(f"content first index type must be 'str' but you entered object with type ({type(content[0])})")

        
        if index_of_content is None and content is not None:
            if self._isthere(panel_name , content[1] , content[0]):
                index_of_content = self._get_widget_index(content[0] , panel_name , content[1])
            else:
                raise ValueError(f"In {panel_name} panel there is not any {content[1]} class with name '{content[0]}'")
        if hasattr(self.panels[panel_name].content[index_of_content] , attr):
            setattr(self.panels[panel_name].content[index_of_content], attr , value)
        else:
            raise AttributeError(f"type '{self.panels[panel_name].content[index_of_content]}' don't have attribute with name '{attr}'")

    def set_content_event(self , panel_name = '' , index_of_content = None , content = None , event = '' , handler = None):
        """
        You should use this method when you want to assign an
        event-driven value to an event-driven property of widgets.
        events like '.on_click' , '.on_value_changed' and etc.
        * How to use :
                    The method of using this method is the same as the 'set_content_attr' method, 
                    except that instead of entering a 'attr', you must enter a 'handler' that is a function.
        """
        error = "One of the arguments index_of_content and content must have value!!"
        help1 = "content must be a tuple like ('content_name' , content_class)"
        help2 = "index_of_content must be integer"
        help3 = "if index_of_content and content , content becomes None and index_of_content is considered"

        if index_of_content is not None and content is not None:
            content = None
        if index_of_content is None and content is None:
            raise ValueError(f"{error} Use this guid :\n\t1){help1}\n\t2){help2} \n\t3){help3}")
        if index_of_content is None and not isinstance(content , tuple):
            raise ValueError(f"{help1}. But you enterd {content} that type is {type(content)}")
        if not isinstance(index_of_content , int) and content is None:
            raise ValueError(f"{help2}. But you enterd {content} that type is {type(content)}")
        if isinstance(content , tuple):
            if len(content) > 2 or len(content) < 2:
                raise ValueError(f"content must have 2 index like ('content_name' , content_class)")
            if not isinstance(content[0] , str):
                raise ValueError(f"content first index type must be 'str' but you entered object with type ({type(content[0])})")

        if index_of_content is None and content is not None:
            if self._isthere(panel_name , content[1] , content[0]):
                index_of_content = self._get_widget_index(content[0] , panel_name , content[1])
            else:
                raise ValueError(f"In {panel_name} panel there is not any {content[1]} class with name '{content[0]}'")

        if hasattr(self.panels[panel_name].content[index_of_content] , event):
            setattr(self.panels[panel_name].content[index_of_content], event , handler)
        else:
            raise AttributeError(f"type '{self.panels[panel_name].content[index_of_content]}' don't have attribute with name '{event}'")

    def button_connection(self , button_panel : str , target_panel : str , button_index):
        if button_index == None : return
        self.panels[button_panel].content[button_index].on_click = lambda : self.enabel_panel(target_panel)

    def get_widget_value(self , Panel_name : str , widget_name : str , widget_class , attr = ""):
        index = self._get_widget_index(name = widget_name , panel_name = Panel_name , widget_type = widget_class)
        if index is not None:
            if hasattr(self.panels[Panel_name].content[index] , attr):
                return getattr(self.panels[Panel_name].content[index] , attr)
            

    def hide_panels(self):
        for key in list(self.panels.keys()):
            self.panels[key].enabled = False
    
    def destroy_panels(self):
        for key , value in list(self.panels.items()):
            destroy(self.panels[key])
    
    def _isthere(self , panel_name , widget_type , widget_name):
        for value in list(self.panels[panel_name].content):
            if not isinstance(value , widget_type) :  continue
            if value.name == widget_name : return True
            else : continue
        return False
    
    def _get_widget_index(self , name , panel_name , widget_type = None):
        for index , value in enumerate(list(self.panels[panel_name].content)):
            if widget_type != None:
                if not isinstance(value , widget_type): continue
            if value.name == name:
                return index

app = Ursina()

panel_manager = PanelManager()
panel_manager.add_panels(
                        name = WindowPanel(title="Panel name" , content = (
                                            Text(name = "name_text" , text = "panel name") , 
                                            Button( name = 'panel_age' , text = 'Go to age panel') , 
                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                            ) , enabled = False
                                        ) ,
                        age = WindowPanel(title= "Panel age" , content = (
                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                            Text(name = "age_text" , text = "panel age"),
                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                            ) , enabled = False
                                        ) ,
                        city = WindowPanel(title= "Panel city" , content = (
                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                            Button( name = 'panel_age' , text = 'Go to age panel') ,
                                            Text(name = "city_text" , text ="panel city")
                                            ) , enabled = False
                                        )
                        )
panel_manager.connect_panel_buttons(panel_name = 'name' , panel_age = 'age' , panel_city = 'city')
panel_manager.enabel_panel('name')
panel_manager.set_position(x = 0.55 , y = 0.45)
panel_manager.set_content_attr(panel_name = 'age' , index_of_content = 1 , attr='text' , value="Here is age panel")
panel_manager.set_content_attr(panel_name = 'city' , content=('city_text' , Text) , attr='text' , value="Here is panel city")

print(panel_manager.get_widget_value(Panel_name = 'age' , widget_name='age_text' , widget_class=Text , attr='text'))
app.run()