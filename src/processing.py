#    This file is part of Wikipie 1.0.
#    Copyright (C) 2018  Carine Dengler
#
#    Wikipie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Multi-threaded wikitext processing.
"""


# standard library imports
import sys
import logging
import configparser
import multiprocessing

# third party imports
# library specific imports


class Processor(object):
    """Multi-threaded wikitext processor.

    :cvar int BATCH_SIZE: batch size
    :ivar Namespace args: command-line arguments
    :ivar Queue queue: queue
    """
    BATCH_SIZE = 100

    def __init__(self):
        """Initialize multi-threaded wikitext processor.

        :param Namespace args: command-line arguments
        """
        try:
            logger = self.get_logger(__name__)
            self.args = args
            self.queue = multiprocessing.JoinableQueue()
            logger.info("fill queue")
            for job in self._get_jobs():
                self.queue.put(job)
            # put sentinels on the queue
            for _ in range(self.args.processes):
                self.queue.put(None)
        except Exception as exception:
            raise RuntimeError(
                "failed to initialize multi-threaded wikitext processor"
            )
        return

    @staticmethod
    def get_logger(suffix):
        """Get multi-threaded logger.

        :param str suffix: suffix

        :returns: logger
        :rtype: Logger
        """
        try:
            logger = multiprocessing.get_logger().getChild(suffix)
            logger.setLevel(logging.INFO)
            logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        except Exception:
            raise RuntimeError("failed to get multi-threaded logger")
        return logger

    def _get_jobs(self):
        """Get jobs."""
        raise NotImplementedError

    def _process(self):
        """Process jobs."""
        try:
            logger = self.get_logger(__name__)
            pid = os.getpid()
            for job in iter(self.queue.get, None):
                logger.info("worker %s processes job %s", pid, job)
                # TODO function
                self.queue.task_done()
            logger.info("worker %s emptied queue", pid)
            self.queue.task_done()
            logger.info("worker %s unblocked queue", pid)
        except Exception as exception:
            logger.exception("worker %s failed to process jobs", pid)
            raise RuntimeError("worker {} failed to process jobs".format(pid))
        return

    def process(self):
        """Process jobs."""
        try:
            logger = self.get_logger(__name__)
            logger.info("process jobs")
            workers = []
            for _ in range(self.args.processes):
                workers.append(
                    multiprocessing.Process(target=self._process, daemon=True)
                )
                workers[-1]
            self.queue.join()
            for worker in workers:
                worker.join()
        except Exception as exception:
            logger.exception("failed to process jobs")
            raise RuntimeError("failed to process jobs")
        return
