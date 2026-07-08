import os
import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق المهام اليومية 📝"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # قائمة لتخزين المهام في الذاكرة
    tasks_list = ft.Column()

    # دالة لحذف المهمة عند الضغط على "حذف"
    def delete_clicked(e, row_control):
        tasks_list.controls.remove(row_control)
        page.update()

    # دالة مساعدة لإنشاء سطر المهمة مع زر الحذف
    def create_task_row(text_value):
        row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        chk = ft.Checkbox(label=text_value)
        
        # استخدام ElevatedButton بالصيغة القديمة المضمونة بالسيرفر
        btn_del = ft.ElevatedButton(
            "حذف", 
            color="white",
            bgcolor="red",
            on_click=lambda e: delete_clicked(e, row)
        )
        
        row.controls = [chk, btn_del]
        return row

    # حقل إدخال المهمة الجديدة
    task_input = ft.TextField(hint_text="ماذا تريد أن تفعل اليوم؟", expand=True)

    # دالة إضافة مهمة جديدة
    def add_clicked(e):
        if task_input.value.strip() != "":
            new_row = create_task_row(task_input.value.strip())
            tasks_list.controls.append(new_row)
            task_input.value = ""
            page.update()

    # واجهة التطبيق الأصلية والبسيطة التي نجحت معك
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
