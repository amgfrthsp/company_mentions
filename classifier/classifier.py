import asyncio
import logging

import logic

# define logging format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    await logic.initialize_database()

    await logic.classify_all()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == '__main__':
    main()
