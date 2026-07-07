import os
import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق المهام اليومية 📝"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # قائمة لتخزين المهام
    tasks_list = ft.Column()

    # حقل إدخال المهمة الجديدة
    task_input = ft.TextField(hint_text="ماذا تريد أن تفعل اليوم؟", expand=True)

    # دالة إضافة مهمة جديدة
    def add_clicked(e):
        if task_input.value.strip() != "":
            tasks_list.controls.append(ft.Checkbox(label=task_input.value))
            task_input.value = ""
            page.update()

    # واجهة التطبيق بألوان نصوص مباشرة ومضمونة
    page.add(
        ft.Row(
            [
                ft.Text("قائمة المهام اليومية 📝", size=30, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                task_input,
                ft.ElevatedButton("إضافة", on_click=add_clicked, bgcolor="blue", color="white")
            ]
        ),
        tasks_list
    )

# السطر السحري لتشغيل السيرفر بنجاح
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
