# wrap_gradio

Wrapping [gradio](https://www.gradio.app/) to create applications with more flexible and clean implementations.

- [wrap\_gradio](#wrap_gradio)
  - [Features](#features)
  - [Usage](#usage)
  - [Description](#description)
    - [LayoutBase](#layoutbase)
      - [Variables](#variables)
      - [Functions](#functions)
    - [Application](#application)
      - [Variables](#variables-1)
      - [Functions](#functions-1)
  - [Example](#example)
    - [Layout of the Example Application](#layout-of-the-example-application)

## Features

- You have global access to all of the components in the ```attach_event``` functions.
- You can structure your gradio application more readable and it can be maintained easily.
- You can reuse your components across the application.

## Usage

- [x] You can check the example from the ```main.py``` file.

- Create a main application with the ```warp_gradio.application.Application``` class.
- Use the layouts from the ```warp_gradio.layouts``` rather than ```gradio``` package. You can use ```RowLayout```, ```ColumnLayout``` and ```TabLayout``` classes.
  - [x] To use the layouts with the ```attach_event``` function, create classes that inherits from these classes. If you are using child layouts which are implented the ```attach_event``` function, call this functions from the parent layouts' ```attach_event``` function.
- Add the components which are created from the ```gradio``` package to layouts with the ```add_component``` function. Add the layers which are created from the ```war_gradio.layouts``` with the ```add_layout``` function.
  - [x] The components have to be created with ```render = false``` parameter, because they are going to be rendered afterwards.
- Add the layouts to the main application with the ```add``` funciton.
- Launch the program with the ```launch``` function.

## Description

- Main classes that used for warping are ```LayoutBase``` and ```Application```.
- Below parts are describing their variables, functions and how they are implemented.

### LayoutBase

- This class is the base class for the layouts which are ```RowLayout```, ```ColumnLayout```, ```TabLayout```.
  
#### Variables

|       Variable       |              Type              | Definition                                                                                                                                                       |
| :------------------: | :----------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     main_layout      |      gradio.blocks.Block       | Stores the main layout from the gradio package of this class. For example storing ```gradio.Row``` layout for the ```RowLayout``` class.                         |
|         name         |              str               | Name of the class. Using for differantiate from other classes and debug purposes.                                                                                |
| global_children_dict | Dict[str, gradio.blocks.Block] | Stores the children components with name. Its values are accumulating with each upper parent.                                                                    |
|     renderables      |              list              | Stores the renderable elements. Layout and children components are not seperated because the order is important. So containing all of them in one list variable. |

#### Functions

```python
def add_component(self, name: str, component: Block) -> None:
    self.renderables.append(component)
    self.global_children_dict[name] = component
```

- In this function, new component is added to layout class.
- This component can be Textbox, TextArea, any component from the gradio package.
- If the ```Block``` component confuse you, the components and layouts in the gradio package are inherit from the ```gradio.blocks.Block``` class.
- You can see from this function new component is added to ```renderables``` and ```global_children_dict``` variables. In the ```add_layout``` function, you will understand why there are two different variables for the children components.

------------------------------------------

```python
def add_layout(self, layout: LayoutBase) -> None:
    self.renderables.append(layout)
    self.global_children_dict.update(layout.global_children_dict)
```

- In this function, new layout is added as children component.
- As you can see, ```global_children_dict``` variable is updating the dictionary with the added new layout's ```global_children_dict``` variable. With this functionality, the parent class includes all the components that children layouts have. You can see in the ```_attach_event``` function why this is important.

------------------------------------------

```python
def render(self) -> None:
    with self.main_layout:
      for renderable in self.renderables:
        renderable.render()

    self.main_layout.render()
```

- In this function, components in the ```renderables``` are rendered under the ```main_layout``` variable.
- ```with``` functionality in the ```gradio.blocks.Block``` is setting the ```Context.block```. This syntax is important because we are rendering not as we initialize the component but after with ```render``` function. So we have to set the ```Context.block``` to render the component as we wanted. If we did not use the ```with``` functionality then the components are rendered with the column style. Why? Because the default style is column style.
- We render the ```renderables``` and then we render the ```main_layout``` because we have just rendered the children components, or ```renderables``` as their variable name, so we have to render the main ```Context.block``` as well.

------------------------------------------

```python
def attach_event(self, block_dict: Dict[str, Block]) -> None:
    raise NotImplementedError
```

- The ```attach_event``` function is leaved as not implemented because it is more specific to class so each class has to implement their ```attach_event``` function.
- You can see what is the ```block_dict``` variable in the ```_attach_event``` function in the ```Application``` class.

### Application

- Base class for the application. You can add the layouts and launch the program.

#### Variables

| Variable |       Type       | Definition                                                                            |
| :------: | :--------------: | :------------------------------------------------------------------------------------ |
|   app    |  gradio.Blocks   | Base application component from the gradio package. It is used to launch the program. |
| children | list[LayoutBase] | Stores the layouts                                                                    |

#### Functions

- Passing the ```add``` function, because it is just adding the given layout to the ````children``` variable.

------------------------------------------

```python
def _render(self):
    with self.app:
        for child in self.children:
            child.render()

    self.app.render()
```

- As we can see from the ```render``` function from the ```LayoutBase``` class, this ```_render``` function is implemented as same as the ```render``` function.

------------------------------------------

```python
def _attach_event(self):
    block_dict: Dict[str, Block] = {}

    for child in self.children:
        block_dict.update(child.global_children_dict)

    with self.app:
        for child in self.children:
            try:
                child.attach_event(block_dict=block_dict)
            except NotImplementedError:
                print(f"{child.name}'s attach_event is not implemented")
```

- In this function, the components are gathered in one dictionary and passed to all children with ```attach_event``` function.
- You can see why the ```global_children_list``` is used in the ```LayoutBase``` class. With this, all of the components in the application is gathered into one dictionary so the component can access all the components with names which is used with inserting into dictionary.
- If the layout is not implent the ```attach_event``` function, the class prints a message with the name which is assigned in the class to inform the developer.

------------------------------------------

- ```launch``` function is not interested one because it is just calling the ```_render``` and ```_attach_event``` functions with the ```launch``` function from the ```gradio.Blocks``` class and starts the application.

## Example

- You can see the example in the ```main.py``` file.

### Layout of the Example Application

- This is the layout of the example application which is taken from ```gui.app.get_config_file()["layout"]```.

```
{'children': [{'children': [{'children': [{'children': [{'children': [{'id': 3},
                                                                      {'id': 4}],
                                                         'id': 9}],
                                           'id': 2}],
                             'id': 1},
                            {'children': [{'children': [{'children': [{'id': 7},
                                                                      {'id': 8}],
                                                         'id': 10}],
                                           'id': 6}],
                             'id': 5}],
               'id': 11}],
 'id': 0}
```

- You can there are bunch of ids so here is the created components with their ids.

```
First Tab Main   Layout   ID : 1
First Tab Row    Layout   ID : 2
First Tab Left   Textbox  ID : 3
First Tab Right  Textbox  ID : 4

Second Tab Main  Layout   ID : 5
Second Tab Row   Layout   ID : 6
Second Tab Left  Textbox  ID : 7
Second Tab Right Textbox  ID : 8
```

- As you can see from the layout the components are structured as we wanted. But you can see there are additional ids which are 0, 9, 10 and 11.

- The ```id : 0``` is the main application which is ```gradio.Blocks```.
- The ```id : 11``` is the ```gradio.layouts.tabs.Tabs``` class. This is inserted here because the ```gradio.layouts.tabs.Tab``` is expecting a parent which is ```gradio.layouts.tabs.Tabs``` class. This can be verified with the ```gradio.layouts.tabs.Tab.get_expected_parent``` function.
- ```id : 9``` and ```id : 10``` are the ```gradio.layouts.form.Form``` classes. These are inserted because the ```gradio.components.textbox.Textbox``` components are expecting a parent which is ```gradio.layouts.form.Form``` class. This can be verified with the ```get_expected_parent``` function from the Textbox component. If you want to see the real implemantation, look at the ```gradio.components.base.FormComponent.get_expected_parent``` function.
