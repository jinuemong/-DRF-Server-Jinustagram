from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from datetime import datetime, timedelta
from  posting.models import Story 

#반복, 자동적으로 실행할 코드 
def del_story():
    isDel = Story.objects.filter(uploadTime__lt = datetime.now()-timedelta(days=1)).delete()
    if isDel[0]>0:
        print("Delete storys objects older then 1 days ")
    else:
        print("no Delete storys")

#10분마다 시간 초과 스토리 삭제 코드 실행 
def start():
    print("jobs.updater.jobs")
    scheduler = BackgroundScheduler()
    scheduler.add_job(del_story,'cron',minute=10)
    scheduler.start()