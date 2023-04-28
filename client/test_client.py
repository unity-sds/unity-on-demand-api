#!/usr/bin/env python
import pytest
import logging

from unity_on_demand_client import Client
from unity_on_demand_client.api.test import echo
from unity_on_demand_client.api.on_demand_v0_1_0 import (
    create_prewarm_request,
    get_prewarm_request,
    cancel_prewarm_request,
)


# create client
client = Client(base_url="http://localhost:8000")


def test_echo():
    r = echo.sync(client=client, echo_str="test this")
    logging.info(f"response: {r}")
    assert r.success == True


@pytest.fixture
def response():
    return create_prewarm_request.sync(client=client, node_count=4)


def test_create_prewarm_request(response):
    logging.info(f"response: {response}")
    assert response.success == True


def test_get_prewarm_status(response):
    r = get_prewarm_request.sync(client=client, request_id=response.request_id)
    logging.info(f"response: {r}")


def test_cancel_prewarm_status(response):
    r = cancel_prewarm_request.sync(client=client, request_id=response.request_id)
    logging.info(f"response: {r}")


@pytest.fixture
def response_additive():
    return create_prewarm_request.sync(client=client, node_count=1, additive=True)


def test_create_prewarm_request_additive(response_additive):
    logging.info(f"response_additive: {response_additive}")
    assert response_additive.success == True


def test_get_prewarm_status_additive(response_additive):
    r = get_prewarm_request.sync(client=client, request_id=response_additive.request_id)
    logging.info(f"response_additive: {r}")


def test_cancel_prewarm_status_additive(response_additive):
    r = cancel_prewarm_request.sync(client=client, request_id=response_additive.request_id)
    logging.info(f"response_additive: {r}")
