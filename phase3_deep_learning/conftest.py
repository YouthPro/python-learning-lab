"""Phase 3 acceptance runs are CPU-based and reject accidental network use."""

import socket
import urllib.request

import pytest
import torch


@pytest.fixture(autouse=True)
def offline_cpu_tests(monkeypatch):
    """Permit local multiprocessing IPC but reject internet sockets/downloads."""
    previous_threads = torch.get_num_threads()
    torch.set_num_threads(2)
    original_connect = socket.socket.connect

    def connect(sock, address):
        if sock.family in {socket.AF_INET, socket.AF_INET6}:
            raise AssertionError(f"Phase 3 tests must be offline: {address}")
        return original_connect(sock, address)

    def no_download(*args, **kwargs):
        raise AssertionError("automated tests must not download data or weights")

    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(urllib.request, "urlopen", no_download)
    monkeypatch.setattr(torch.hub, "download_url_to_file", no_download)
    yield
    torch.set_num_threads(previous_threads)
