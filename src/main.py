import os
import sys
from crontab import CronTab
from bot import bot_job

JOBS_INTERVAL = 20


def main():
    python_interpreter = sys.executable
    working_directory = os.getcwd()

    cron = CronTab(user=True)

    extractor_script = os.path.join(working_directory, "extractor", "extractor_job.py")

    extractor_job = cron.new(command=f"cd {working_directory} && {python_interpreter} {extractor_script}")
    extractor_job.minute.every(JOBS_INTERVAL)

    classifier_script = os.path.join(working_directory, "classifier", "classifier_job.py")

    classifier_job = cron.new(command=f"cd {working_directory} && {python_interpreter} {classifier_script}")
    classifier_job.minute.during(10, 59).every(JOBS_INTERVAL)

    cron.write()

    bot_job.main()


if __name__ == '__main__':
    main()
