import flet as ft
import os  # مكتبة مهمة لقراءة إعدادات سيرفر الإنترنت تلقائياً

def main(page: ft.Page):
    # إعدادات الصفحة الأساسية وشكل التطبيق
    page.title = "تطبيق مهامي اليومية المطور 🚀"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT 
    
    # عنوان التطبيق والمكان المخصص لعرض المهام
    title = ft.Text(value="قائمة المهام اليومية 📝", size=24, weight=ft.FontWeight.BOLD, color="#2c3e50")
    tasks_view = ft.ListView(expand=1, spacing=10, padding=20)

    # دالة لتحديث شكل ولون المهمة عند وضع علامة صح عليها
    def checkbox_changed(e):
        if e.control.value == True:
            # يتحول النص للون رمادي فاتح ويوضع عليه خط عند الانتهاء
            e.control.label_style = ft.TextStyle(italic=True, color="#bdc3c7", decoration=ft.TextDecoration.LINE_THROUGH)
        else:
            # يعود للونه الأصلي عند إزالة علامة الصح
            e.control.label_style = ft.TextStyle(italic=False, color="#2c3e50", decoration=ft.TextDecoration.NONE)
        page.update() 

    # دالة لحذف المهمة بالكامل من القائمة عند الضغط على زر X
    def delete_clicked(task_row):
        tasks_view.controls.remove(task_row)
        page.update()

    # دالة لإضافة مهمة جديدة إلى القائمة
    def add_clicked(e):
        if new_task.value.strip() != "": 
            # إنشاء مربع الاختيار (الصح) الخاص بالمهمة
            task_checkbox = ft.Checkbox(
                label=new_task.value,
                value=False,
                label_style=ft.TextStyle(color="#2c3e50", size=16),
                on_change=checkbox_changed 
            )
            
            # ترتيب المكونات في سطر: المهمة على اليسار وزر الحذف على اليمين
            task_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
            # زر الحذف النصي باللون الأحمر لتجنب مشاكل الأيقونات القديمة
            delete_button = ft.TextButton(
                content=ft.Text("X", color="#e74c3c", weight="bold", size=18),
                on_click=lambda _: delete_clicked(task_row)
            )
            
            # دمج المكونات وإضافتها للقائمة الكبيرة
            task_row.controls = [task_checkbox, delete_button]
            tasks_view.controls.append(task_row) 
            new_task.value = ""  # تفريغ مربع الكتابة بعد الإضافة
            new_task.focus()
            page.update() 

    # مكونات إدخال النص والزر الأزرق المخصص للإضافة (+)
    new_task = ft.TextField(hint_text="ماذا تريد أن تنجز اليوم؟ 🤔", expand=True, border_color="#3498db")
    add_button = ft.FloatingActionButton(content=ft.Text("+", size=20, weight="bold"), on_click=add_clicked, bgcolor="#3498db")
    input_row = ft.Row(controls=[new_task, add_button])

    # إضافة كل المكونات إلى شاشة التطبيق
    page.add(
        title,
        ft.Divider(height=10, color="transparent"),
        input_row,
        ft.Divider(height=20),
        tasks_view
    )

# السطر الأخير السحري: يأخذ رقم المنفذ (Port) الممنوح من سيرفر الإنترنت تلقائياً ويشغل التطبيق كموقع ويب
port = int(os.environ.get("PORT", 8550))
ft.app(main)
