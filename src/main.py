import os
import sys
from crontab import CronTab

JOBS_INTERVAL = 20


def main():
    python_interpreter = sys.executable
    current_directory = os.getcwd()

    cron = CronTab(user=True)

    extractor_directory = os.path.join(current_directory, "src", "extractor")
    extractor_script = os.path.join(extractor_directory, "extractor.py")

    extractor_job = cron.new(command=f"cd {extractor_directory} && {python_interpreter} {extractor_script}")
    extractor_job.minute.every(JOBS_INTERVAL)

    classifier_directory = os.path.join(current_directory, "src", "classifier")
    classifier_script = os.path.join(extractor_directory, "classifier.py")

    classifier_job = cron.new(command=f"cd {classifier_directory} && {python_interpreter} {classifier_script}")
    classifier_job.minute.during(10, 59).every(JOBS_INTERVAL)

    cron.write()


if __name__ == '__main__':
    main()
