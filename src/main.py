import os
import sys
from crontab import CronTab

JOBS_INTERVAL = 20


def main():
    python_interpreter = sys.executable
    current_directory = os.getcwd()

    extractor_script = os.path.join(current_directory, "src", "extractor", "extractor.py")
    classifier_script = os.path.join(current_directory, "src", "classifier", "classifier.py")

    cron = CronTab(user=True)
    extractor_job = cron.new(command=f"{python_interpreter} {extractor_script}")
    extractor_job.minute.every(JOBS_INTERVAL)

    classifier_job = cron.new(command=f"{python_interpreter} {classifier_script}")
    classifier_job.minute.during(10, 59).every(JOBS_INTERVAL)
    cron.write()


if __name__ == '__main__':
    main()
