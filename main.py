import os
import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق المهام الاحترافي 📝"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # قائمة لتخزين المهام
    tasks_list = ft.Column()

    # دالة لتغيير لون التطبيق (ليلي / نهاري)
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.text = "الوضع المضيء"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.text = "الوضع الليلي"
        page.update()

    # زر تغيير الألوان (بدون أيقونات لضمان عدم حدوث خطأ)
    theme_btn = ft.ElevatedButton(
        text="الوضع الليلي",
        on_click=change_theme,
        bgcolor="blue",
        color="white"
    )

    # دالة حذف مهمة
    def delete_task(e, task_row):
        tasks_list.controls.remove(task_row)
        page.update()

    # دالة مساعدة لإنشاء سطر المهمة مع زر الحذف
    def create_task_row(task_text):
        task_row = ft.Row(alignment=ft.MainAxisAlignment.BETWEEN)
        chk = ft.Checkbox(label=task_text)
        
        # زر حذف مكتوب كتابة (نص) ليكون مضموناً 100% على السيرفر
        btn_delete = ft.TextButton(
            text="حذف",
            style=ft.ButtonStyle(color="red"),
            on_click=lambda e: delete_task(e, task_row)
        )
        
        task_row.controls = [chk, btn_delete]
        return task_row

    # دالة إضافة مهمة جديدة
    def add_clicked(e):
        if task_input.value.strip() != "":
            new_row = create_task_row(task_input.value.strip())
            tasks_list.controls.append(new_row)
            task_input.value = ""
            page.update()

    # حقل إدخال المهمة الجديدة
    task_input = ft.TextField(hint_text="ماذا تريد أن تفعل اليوم؟", expand=True)

    # واجهة التطبيق
    page.add(
        ft.Row([theme_btn], alignment=ft.MainAxisAlignment.END),
        ft.Row(
            [
                ft.Text("قائمة المهام اليومية 📝", size=30, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                task_input,
                ft.ElevatedButton("إضافة", on_click=add_clicked, bgcolor="green", color="white")
            ]
        ),
        ft.Divider(),
        tasks_list
    )

# العودة للسطر السحري القياسي الذي نجح في البداية
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
