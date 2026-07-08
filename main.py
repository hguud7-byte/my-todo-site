import os
import json
import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق المهام اليومية 📝"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # قائمة لتخزين المهام
    tasks_list = ft.Column()

    # دالة لحفظ المهام في ذاكرة المتصفح
    def save_tasks():
        tasks_data = []
        for ctrl in tasks_list.controls:
            if isinstance(ctrl, ft.Row):
                checkbox = ctrl.controls[0]
                tasks_data.append({"label": checkbox.label, "value": checkbox.value})
        page.client_storage.set("saved_tasks", json.dumps(tasks_data))

    # دالة لحذف المهمة عند الضغط على "حذف"
    def delete_clicked(e, row_control):
        tasks_list.controls.remove(row_control)
        save_tasks()
        page.update()

    # دالة لتحديث الحفظ عند تغيير حالة التشيك بوكس
    def checkbox_changed(e):
        save_tasks()

    # دالة مساعدة لإنشاء سطر المهمة مع زر الحذف بنفس طريقة الكود القديم
    def create_task_row(text_value, is_checked=False):
        row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        chk = ft.Checkbox(label=text_value, value=is_checked, on_change=checkbox_changed)
        
        btn_del = ft.TextButton(
            text="حذف", 
            style=ft.ButtonStyle(color="red"), 
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
            save_tasks()
            page.update()

    # تحميل المهام المحفوظة تلقائياً عند فتح الموقع
    saved_data = page.client_storage.get("saved_tasks")
    if saved_data:
        try:
            tasks_data = json.loads(saved_data)
            for item in tasks_data:
                tasks_list.controls.append(create_task_row(item["label"], item["value"]))
        except:
            pass

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

# 👈 السطر السحري القديم والأصلي لتشغيل السيرفر مكانه هنا في النهاية
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
