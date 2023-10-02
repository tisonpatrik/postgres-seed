"""
Utility functions for executing tasks with logging.
These functions are used to handle both asynchronous and synchronous operations.
"""

import logging

from fastapi import HTTPException, status


async def execute_with_logging_async(task, *args, start_msg, end_msg):
    """Helper function to wrap asynchronous task execution with logging."""
    logging.info(start_msg)

    try:
        await task(*args)
    except Exception as exc:
        logging.error("Error occurred: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request.",
        ) from exc

    logging.info(end_msg)


def execute_with_logging(task, *args, start_msg, end_msg):
    """Helper function to wrap synchronous task execution with logging."""
    logging.info(start_msg)

    try:
        task(*args)
    except Exception as exc:
        logging.error("Error occurred: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request.",
        ) from exc

    logging.info(end_msg)
