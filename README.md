# wrap_gradio
Wrapping [gradio](https://www.gradio.app/) to create gradio applications with more flexible and clean implementations.

## How it is wrapped?

### LayoutBase

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
