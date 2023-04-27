from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.echo_response import EchoResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    echo_str: str,
) -> Dict[str, Any]:
    url = "{}/test/echo".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["echo_str"] = echo_str

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, EchoResponse, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = EchoResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, EchoResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    echo_str: str,
) -> Response[Union[Any, EchoResponse, HTTPValidationError]]:
    """Echo

    Args:
        echo_str (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EchoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        echo_str=echo_str,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    echo_str: str,
) -> Optional[Union[Any, EchoResponse, HTTPValidationError]]:
    """Echo

    Args:
        echo_str (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EchoResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        echo_str=echo_str,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    echo_str: str,
) -> Response[Union[Any, EchoResponse, HTTPValidationError]]:
    """Echo

    Args:
        echo_str (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, EchoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        echo_str=echo_str,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    echo_str: str,
) -> Optional[Union[Any, EchoResponse, HTTPValidationError]]:
    """Echo

    Args:
        echo_str (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, EchoResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            echo_str=echo_str,
        )
    ).parsed
