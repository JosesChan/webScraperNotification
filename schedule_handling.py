from apscheduler.schedulers.background import BlockingScheduler

def scheduleProgram(inputScript):
    sched = BlockingScheduler()

    # Store the job in a variable in case we want to cancel it
    sched.add_job(inputScript, 'cron', minute='0,15,30,45')

    sched.start()