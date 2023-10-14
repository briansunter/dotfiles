from datetime import datetime, timedelta

start_date = datetime(2023,1,1)

week_templates = []
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

current_month = start_date.month
for week in range(1, 53):
    end_date = start_date + timedelta(days=6)
    if start_date.month != end_date.month:
        end_date = end_date.replace(day=1) - timedelta(days=1)
        
    week_template = f"[[{start_date.year}/week/{week}]]"
    
    if start_date.month != current_month:
        current_month = start_date.month
        week_templates.append(month_names[current_month - 1])

    week_templates.append(week_template)
    start_date = end_date + timedelta(days=1)


for week_template in week_templates:
    print(week_template)