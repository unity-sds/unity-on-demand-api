from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.prewarm_response import PrewarmResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    node_count: Union[Unset, None, int] = 1,
    additive: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/on-demand/v010/prewarm".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["node_count"] = node_count

    params["additive"] = additive

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, PrewarmResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PrewarmResponse.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = cast(Any, None)
        return response_501
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, PrewarmResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    node_count: Union[Unset, None, int] = 1,
    additive: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        node_count (Union[Unset, None, int]):  Default: 1.
        additive (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        node_count=node_count,
        additive=additive,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    node_count: Union[Unset, None, int] = 1,
    additive: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        node_count (Union[Unset, None, int]):  Default: 1.
        additive (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PrewarmResponse]
    """

    return sync_detailed(
        client=client,
        node_count=node_count,
        additive=additive,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    node_count: Union[Unset, None, int] = 1,
    additive: Union[Unset, None, bool] = False,
) -> Response[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        node_count (Union[Unset, None, int]):  Default: 1.
        additive (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        node_count=node_count,
        additive=additive,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    node_count: Union[Unset, None, int] = 1,
    additive: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        node_count (Union[Unset, None, int]):  Default: 1.
        additive (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, PrewarmResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            node_count=node_count,
            additive=additive,
        )
    ).parsed
