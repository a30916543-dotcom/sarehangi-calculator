
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
import ast
import operator

Window.clearcolor = (0.82, 0.94, 0.82, 1)

# محاسبه امن عبارت‌های ریاضی
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def calculate(node):
    if isinstance(node, ast.Expression):
        return calculate(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](
            calculate(node.left), calculate(node.right)
        )
    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        value = calculate(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("عبارت نامعتبر است")


class CalculatorApp(App):
    def build(self):
        self.title = "ماشین حساب سرهنگی"

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        title = Label(
            text="ماشین حساب سرهنگی",
            font_size=25,
            color=(0.1, 0.25, 0.1, 1),
            size_hint_y=0.16
        )
        root.add_widget(title)

        self.display = Label(
            text="0",
            font_size=34,
            color=(0.05, 0.05, 0.05, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.23
        )
        self.display.bind(size=self.update_text_size)
        root.add_widget(self.display)

        grid = GridLayout(cols=4, spacing=7)
        grid_rows = [
            ["C", "⌫", "(", ")"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "=", "+"],
        ]

        for row in grid_rows:
            for value in row:
                button = Button(
                    text=value,
                    font_size=25,
                    background_normal="",
                    background_color=(
                        (1.0, 0.57, 0.18, 1)
                        if value in ["÷", "×", "−", "+", "="]
                        else (0.96, 0.72, 0.38, 1)
                        if value in ["C", "⌫"]
                        else (1.0, 0.83, 0.58, 1)
                    ),
                    color=(0.12, 0.12, 0.12, 1)
                )
                button.bind(on_release=self.press)
                grid.add_widget(button)

        root.add_widget(grid)
        return root

    def update_text_size(self, instance, size):
        instance.text_size = size

    def press(self, button):
        value = button.text
        current = self.display.text

        if value == "C":
            self.display.text = "0"
        elif value == "⌫":
            self.display.text = current[:-1] or "0"
        elif value == "=":
            try:
                expression = (
                    current.replace("×", "*")
                    .replace("÷", "/")
                    .replace("−", "-")
                )
                tree = ast.parse(expression, mode="eval")
                result = calculate(tree)
                self.display.text = (
                    str(int(result))
                    if isinstance(result, float) and result.is_integer()
                    else str(result)
                )
            except Exception:
                self.display.text = "خطا"
        else:
            if current in ("0", "خطا"):
                self.display.text = (
                    value if value not in ("+", "×", "÷", "−")
                    else "0" + value
                )
            else:
                self.display.text += value


if __name__ == "__main__":
    CalculatorApp().run()
