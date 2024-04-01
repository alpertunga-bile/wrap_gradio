# wrap_gradio
Wrapping [gradio](https://www.gradio.app/) to create gradio applications with more flexible and clean implementations.

- [wrap\_gradio](#wrap_gradio)
  - [Description](#description)
    - [LayoutBase](#layoutbase)
      - [Variables](#variables)
      - [Functions](#functions)
    - [Application](#application)
      - [Variables](#variables-1)
      - [Functions- wrap\_gradio](#functions--wrap_gradio)
  - [Example](#example)

## Description

- Main classes that used for warping are ```LayoutBase``` and ```Application```.
- So lets see their variables and functions and how they are implemented.

### LayoutBase
- This class is a base class for the layouts which are ```RowLayout```, ```ColumnLayout```, ```TabLayout```.
  
#### Variables
|       Variable       |              Type              | Definition                                                                                                                                |
| :------------------: | :----------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------- |
|     main_layout      |      gradio.blocks.Block       | Stores the main layout from the gradio package of this class. For example storing ```Row``` layout for the ```RowLayout``` class.         |
|         name         |              str               | Name for the class. Just for differantiate from other classes and debug purposes.                                                         |
| global_children_dict | Dict[str, gradio.blocks.Block] | Stores the children components from the below layouts. Its values are accumulating with each parent.                                      |
|     renderables      |              list              | Stores the renderable elements. Layout and children is not seperated because the order is important so containing all of them in one list |

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

```python
def add_layout(self, layout: LayoutBase) -> None:
    self.renderables.append(layout)
    self.global_children_dict.update(layout.global_children_dict)
```
- In this function, new layout, which is derived from this class, is added.
- As you can see, ```global_children_dict``` variable is updating the dictionary with the added new layout. With this functionality, the parent has the all components that children layouts have. You can see in the ```attach_event``` function why this is important.

```python
def render(self) -> None:
    with self.main_layout:
      for renderable in self.renderables:
        renderable.render()

    self.main_layout.render()
```
- In this function, components in the ```renderables``` are rendered under the ```main_layout``` variable.
- Now the crucial part, ```with``` functionality in the ```gradio.blocks.Block``` is setting the ```Context.block```. Why it is important? It is important because we are rendering not as we are initialize but after with ```render``` function, we have to set the ```Context.block``` to render the component as we wanted. If we did not use the ```with``` functionality then the components are rendered with as column style. Why? Because the default style is column style.
- Now as we render the ```renderables```, we render the ```main_layout```. Because we have just rendered the children components, or ```renderables``` as their variable name, so we have to render the main ```Context.block``` as well.

```python
def attach_event(self, block_dict: Dict[str, Block]) -> None:
    raise NotImplementedError
``` 
- The ```attach_event``` function is leaved as not implemented because it is more specific to class so each class has to implement their ```attach_event``` function.
- You can see what is the ```block_dict``` variable in the ```attach_event``` function in the ```Application``` class.

### Application

#### Variables

#### Functions- [wrap\_gradio](#wrap_gradio)
- [wrap\_gradio](#wrap_gradio)
  - [Description](#description)
    - [LayoutBase](#layoutbase)
      - [Variables](#variables)
      - [Functions](#functions)
    - [Application](#application)
      - [Variables](#variables-1)
      - [Functions- wrap\_gradio](#functions--wrap_gradio)
  - [Example](#example)


## Example
- You can see the example in the ```main.py``` file.
- After the wrapping, the main function will look like this:

```python
gui = Application(title="Wrap Gradio")

first_tab = FirstTab(label="First Tab")
second_tab = SecondTab(label="Second Tab")

gui.add(first_tab)
gui.add(second_tab)

gui.launch()
```
