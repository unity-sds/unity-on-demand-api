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
    gpu_needed: Union[Unset, None, bool] = False,
    disk_space_in_gb: Union[Unset, None, int] = 20,
    mem_size_in_gb: Union[Unset, None, int] = 4,
) -> Dict[str, Any]:
    url = "{}/on-demand/v020/prewarm".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["gpu_needed"] = gpu_needed

    params["disk_space_in_gb"] = disk_space_in_gb

    params["mem_size_in_gb"] = mem_size_in_gb

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
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
    gpu_needed: Union[Unset, None, bool] = False,
    disk_space_in_gb: Union[Unset, None, int] = 20,
    mem_size_in_gb: Union[Unset, None, int] = 4,
) -> Response[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        gpu_needed (Union[Unset, None, bool]):
        disk_space_in_gb (Union[Unset, None, int]):  Default: 20.
        mem_size_in_gb (Union[Unset, None, int]):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        gpu_needed=gpu_needed,
        disk_space_in_gb=disk_space_in_gb,
        mem_size_in_gb=mem_size_in_gb,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    gpu_needed: Union[Unset, None, bool] = False,
    disk_space_in_gb: Union[Unset, None, int] = 20,
    mem_size_in_gb: Union[Unset, None, int] = 4,
) -> Optional[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        gpu_needed (Union[Unset, None, bool]):
        disk_space_in_gb (Union[Unset, None, int]):  Default: 20.
        mem_size_in_gb (Union[Unset, None, int]):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    return sync_detailed(
        client=client,
        gpu_needed=gpu_needed,
        disk_space_in_gb=disk_space_in_gb,
        mem_size_in_gb=mem_size_in_gb,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    gpu_needed: Union[Unset, None, bool] = False,
    disk_space_in_gb: Union[Unset, None, int] = 20,
    mem_size_in_gb: Union[Unset, None, int] = 4,
) -> Response[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        gpu_needed (Union[Unset, None, bool]):
        disk_space_in_gb (Union[Unset, None, int]):  Default: 20.
        mem_size_in_gb (Union[Unset, None, int]):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        gpu_needed=gpu_needed,
        disk_space_in_gb=disk_space_in_gb,
        mem_size_in_gb=mem_size_in_gb,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    gpu_needed: Union[Unset, None, bool] = False,
    disk_space_in_gb: Union[Unset, None, int] = 20,
    mem_size_in_gb: Union[Unset, None, int] = 4,
) -> Optional[Union[Any, HTTPValidationError, PrewarmResponse]]:
    """Create Prewarm Request

    Args:
        gpu_needed (Union[Unset, None, bool]):
        disk_space_in_gb (Union[Unset, None, int]):  Default: 20.
        mem_size_in_gb (Union[Unset, None, int]):  Default: 4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, PrewarmResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            gpu_needed=gpu_needed,
            disk_space_in_gb=disk_space_in_gb,
            mem_size_in_gb=mem_size_in_gb,
        )
    ).parsed
