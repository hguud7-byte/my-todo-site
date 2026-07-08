
    import os
import json
import flet as ft

def main(page: ft.Page):
    page.title = "تطبيق المهام الاحترافي 📝"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # دالة لتغيير لون التطبيق (ليلي / نهاري)
    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.icons.SUNNY
            theme_btn.text = "الوضع المضيء"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.icons.DARK_MODE
            theme_btn.text = "الوضع الليلي"
        page.update()

    # زر تغيير الألوان في أعلى الصفحة
    theme_btn = ft.ElevatedButton(
        text="الوضع الليلي",
        icon=ft.icons.DARK_MODE,
        on_click=change_theme,
        bgcolor="blue",
        color="white"
    )

    tasks_list = ft.Column()

    # دالة حفظ المهام في ذاكرة المتصفح
    def save_tasks():
        tasks_data = []
        for ctrl in tasks_list.controls:
            # نستخرج النص وحالة التشيك بوكس
            checkbox = ctrl.controls[0]
            tasks_data.append({"label": checkbox.label, "value": checkbox.value})
        page.client_storage.set("saved_tasks", json.dumps(tasks_data))

    # دالة حذف مهمة معينة
    def delete_task(e, task_row):
        tasks_list.controls.remove(task_row)
        save_tasks()  # حفظ التعديل بعد الحذف
        page.update()

    # دالة تشغيل عند الضغط على التشيك بوكس لحفظ حالته (مكتملة أم لا)
    def checkbox_changed(e):
        save_tasks()

    # دالة مساعدة لإنشاء سطر المهمة (مع زر الحذف)
    def create_task_row(task_text, is_checked=False):
        task_row = ft.Row(alignment=ft.MainAxisAlignment.BETWEEN)
        chk = ft.Checkbox(label=task_text, value=is_checked, on_change=checkbox_changed)
        
        # زر الحذف (أيقونة سلة المهام)
        btn_delete = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color="red",
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
            save_tasks()  # حفظ المهمة الجديدة فوراً
            page.update()

    # تحميل المهام المحفوظة سابقاً عند فتح الموقع
    saved_data = page.client_storage.get("saved_tasks")
    if saved_data:
        try:
            tasks_data = json.loads(saved_data)
            for item in tasks_data:
                tasks_list.controls.append(create_task_row(item["label"], item["value"]))
        except:
            pass

    # حقل إدخال المهمة الجديدة
    task_input = ft.TextField(hint_text="ماذا تريد أن تفعل اليوم؟", expand=True)

    # واجهة التطبيق كاملة
    page.add(
        ft.Row([theme_btn], alignment=ft.MainAxisAlignment.END), # زر الألوان فوق على اليمين
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
        ft.Divider(), # خط فاصل أنيق
        tasks_list
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
