from fastapi import APIRouter, BackgroundTasks, Depends

from auth.base_configs import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # 1400 ms - Чекаємо клієнта
    send_email_report_dashboard(user.username)
    # 500 ms - Завдання виконано на фоні FastAPI в event loop'е
    background_tasks.add_task(send_email_report_dashboard, user.username)
    # 600 ms - Завдання виконано воркером Celery в окремому процесі
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Лист відправлено",
        "details": None
    }